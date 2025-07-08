from fastapi import Depends , HTTPException , status
from passlib.context import CryptContext
from jose import jwt , JWTError
import os 
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime , timedelta
from sqlalchemy.orm import Session
from typing import Optional
from .database import get_session as get_db
from app.user.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = '/auth/login')

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
RESET_SECRET_KEY = os.getenv("RESET_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password : str, hashed : str) -> bool:
    return pwd_context.verify(plain_password , hashed)

def create_access_token(data: dict , expires_delta : Optional[timedelta]= None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes = 15))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY , algorithm=ALGORITHM)

def generate_password_reset_token(email:str) -> str :
    expire = datetime.utcnow() + timedelta(hours=1)
    playload = {"sub" : email , "exp" : expire}
    return jwt.encode(playload , RESET_SECRET_KEY , algorithm= ALGORITHM)

def verify_password_reset_token(token : str) -> str | None :
    try : 
        payload = jwt.decode(token , RESET_SECRET_KEY, algorithms= ALGORITHM)
        return payload.get("sub")
    except JWTError:
        return None


def get_current_user(db : Session= Depends(get_db), token : str = Depends(oauth2_scheme)) -> User :
    credentials_exception = HTTPException (
        status_code = status.HTTP_401_UNAUTHORIZED , 
        detail = "Impossible de valider les informations d'identification",
        headers = {"WWW-Authenticate" : "Bearer"},
    )

    try :
        playload = jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])
        slug : str = playload.get("sub")
        if slug is None : 
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.slug == slug).first()
    if user is None or not user.is_active : 
        raise credentials_exception
    return user