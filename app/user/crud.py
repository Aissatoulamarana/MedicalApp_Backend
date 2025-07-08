from sqlmodel import Session, select 
from .models import User 
from .schemas import UserCreate, UserUpdate
from app.core.security import hash_password


def create_user(db: Session, user:UserCreate) -> User :
    hashed_pw = hash_password(user.password)
    db_user = User(**user.dict(exclude={"password"}), password = hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_slug(db: Session, slug: str) -> User | None:
    return db.exec(select(User).where(User.slug == slug)).first()

def get_user_by_email(db: Session, email : str) -> User | None :
    return db.exec(select(User).where(User.email == email)).first()

def list_users(db: Session) -> list[User]:
    return db.exec(select(User)).all()

def update_user(db: Session, slug : str, user_update : UserUpdate) -> User | None:
    user = get_user_by_slug(db, slug)
    if user:
        update_data = user_update.dict(exclude_unset = True)
        for key, value in update_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return(user)
    return None

def delete_user(db : Session, slug : str) -> bool:
    user = get_user_by_slug(db, slug)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False