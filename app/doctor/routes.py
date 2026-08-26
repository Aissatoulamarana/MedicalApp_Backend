from fastapi import APIRouter , Depends , HTTPException 
from sqlmodel import Session
from . import crud , schemas
from app.user.models import User
from app.user.crud import get_user_by_email
from app.hospital.models import Hospital
from app.hospital.crud import get_hospital_by_slug
from app.core.database import get_session as get_db
from app.utils.emails import send_email

router = APIRouter(prefix = "/doctors" , tags=["doctors"])

@router.post("/", response_model = schemas.DoctorRead)
def create_doctor(doctor: schemas.DoctorCreate , db : Session = Depends(get_db)):
    existing_user = get_user_by_email(db , doctor.email)
    if existing_user:
        raise HTTPException(status_code = 400, detail = "Un utilisateur avec cet email existe déja")
    
    hospital = get_hospital_by_slug(db, doctor.hospital_slug)
    if not hospital:
        raise HTTPException(status_code = 404 , detail = "Hôpital Introuvable")
    
    new_doctor = crud.create_doctor(db , doctor)

    html_body = f""" 
    <p>Bonjour {doctor.first_name},</p>
    <p> Vous venez de créer votre compte sur notre plateforme.</p>
    <p> Merci de bien vouloir patienter que nous verifions vos informations</p>
    <p> afin d'activer votre compte . </p>
    <p> Un e-mail vous sera communiqué dans les prochains instants </p>
    <p> Merci & Bienvenue 😊 </p>
    """
    send_email(
        subject= "Inscription sur MedicalApp",
        to = doctor.email,
        body= html_body
    )
    
    return new_doctor

@router.post("/{slug}" , response_model = schemas.DoctorRead)
def activate_doctor(slug : str , db: Session = Depends(get_db)):
    doctor = crud.activate_doctor(db, slug)
    if not doctor :
        raise HTTPException(status_code = 404 , detail = "Docteur Introuvable")

    return doctor

@router.get("/", response_model = list[schemas.DoctorRead])
def list_doctors(db: Session = Depends(get_db)):
    return crud.list_doctors(db)

@router.patch("/{slug}" , response_model = schemas.DoctorRead)
def update_doctor(slug : str , updates : schemas.DoctorUpdate , db: Session = Depends(get_db)):
    return crud.update_doctor(db , updates , slug)