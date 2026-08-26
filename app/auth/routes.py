from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import Session
from app.core.security import create_access_token, create_refresh_token , generate_password_reset_token , verify_password_reset_token , hash_password , get_current_user
from app.core.database import get_session as get_db
from app.utils.emails import send_email
from . import schemas, crud
from app.user.schemas import UserRead
from app.user.models import User


router = APIRouter(prefix ='/auth', tags=["Auth"])

@router.post("/login", response_model = schemas.TokenResponse)
def login(data: schemas.Login , db :Session = Depends(get_db)):
    user = crud.authenticate_user(db, data.email, data.password)
    if not user : 
        raise HTTPException(status_code = 401, detail = 'Identifiants invalides ou Compte inactif')
    
    access_token = create_access_token({"sub": user.slug})
    refresh_token = create_refresh_token({"sub": user.slug})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type":  "bearer"
    }

@router.post('/reset-password')
def reset_password(data : schemas.PasswordReset , db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code = 404 , detail = 'Utilisateur non trouvé avec cet email')
    token = generate_password_reset_token(user.email)

    reset_link = f"http://localhost:8000/auth/reset-password/confirm?token={token}"
    html_body = f"""
    <p>Bonjour {user.first_name},</p>
    <p> Vous avez demandé à réinitialiser votre mot de passe.</p>
    <p> Cliquez sur le lien ci-dessous pour definir un nouveau mot de passe : </p>
    <a href="{reset_link}">{reset_link}</a>
    <p> Ce lien est valide pendant 1 heure. </p>
    """
    send_email(
        subject= "Réinitialisation de votre mot de passe",
        to = user.email,
        body= html_body
    )

    return {"message": "Un email de réinitialisation à été envoyé"}

@router.post('/reset_password/confirm')
def reset_password_confirm(data : schemas.PasswordResetConfirm , db : Session = Depends(get_db)):
    email = verify_password_reset_token(data.token)
    if not email:
        raise HTTPException(status_code = 400 , detail = 'Token Invalide ou expiré')
    
    user = crud.get_user_by_email(db , email)
    if not user:
        raise HTTPException(status_code = 404 , detail = 'Utilisateur non trouvé')
    
    user.password = hash_password(data.new_password)
    db.add(user)
    db.commit()

    ht_body = f"""
    <p>Bonjour {user.first_name},</p>
    <p> Votre mot de passe a été mis à jour avec succès.</p>
    <p>Vous pouvez vous connecter avec votre nouveau de mot de passe </p>
    <p>On vous remercie</p>
    """
    send_email(
        subject= "Réinitialisation du mot de passe reussie",
        to = user.email,
        body= ht_body
    )

    return {"message": "mot de passe mis a jour avec succès"}

@router.get("/me", response_model = UserRead)
def read_current_user(current_user : User = Depends(get_current_user)):
    return crud.get_user_me(current_user)