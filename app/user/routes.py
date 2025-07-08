from fastapi import APIRouter, Depends, HTTPException , status
from sqlmodel import Session
from . import crud , schemas
from app.core.database import get_session as get_db

router = APIRouter(prefix= "/users" , tags=["users"])

@router.post("/", response_model = schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code = 400 , detail='Email déja existant')
    return crud.create_user(db, user)

@router.get("/{slug}", response_model = schemas.UserRead)
def read_user(slug: str, db:  Session = Depends(get_db)):
    user  = crud.get_user_by_slug(db, slug)
    if not user:
        raise HTTPException(status_code = 404 , detail = 'Utilisateur non trouvé')
    return user

@router.get("/", response_model = list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)

@router.put("/{slug}", response_model = schemas.UserRead)
def update_user(slug : str , updates: schemas.UserUpdate, db : Session = Depends(get_db)):
    user = crud.update_user(db, slug, updates)
    if not user:
        raise HTTPException(status_code = 404, detail= 'Utilisateur introuvable')
    return user

@router.delete('/{slug}')
def delete_user(slug: str, db : Session = Depends(get_db)):
    success = crud.delete_user(db, slug)
    if not success:
        raise HTTPException(status_code = 400 , detail = "Suppression echouée")
    return {"Utilisateur supprimé avec succes"}
