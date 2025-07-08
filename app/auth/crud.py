from app.core.security import verify_password 
from app.user.models import User
from app.user.crud import get_user_by_email
from sqlmodel import Session, select



def authenticate_user(db: Session , email:str , password : str):
    user = get_user_by_email(db, email)
    if not user or not user.is_active:
        return None
    if not verify_password(password, user.password):
        return None
    return  user

def  get_user_me(user : User) -> User : 
    return user 