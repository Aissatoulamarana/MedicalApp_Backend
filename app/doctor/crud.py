from sqlmodel import Session , select
from uuid import uuid4
from fastapi import HTTPException
from .models import Doctor
from .schemas import DoctorCreate, DoctorUpdate
from app.user.models import User , RoleEnum
from app.user.crud import get_user_by_slug
from app.core.security import hash_password
from app.utils.emails import send_email


def create_doctor(db : Session, doctor_data : DoctorCreate) -> Doctor :
    hashed_pw = hash_password(doctor_data.password)

    user = User(
        slug = str(uuid4()),
        first_name = doctor_data.first_name,
        last_name = doctor_data.last_name,
        email = doctor_data.email,
        phone = doctor_data.phone,
        address = doctor_data.address,
        birth_date = doctor_data.birth_date,
        sex = doctor_data.sex,
        role = RoleEnum.DOCTOR,
        password = hashed_pw,
        is_active = False

    )

    db.add(user)
    db.commit()
    db.refresh(user)

    doctor = Doctor(
        user_slug = user.slug,
        hospital_slug = doctor_data.hospital_slug,
        speciality = doctor_data.speciality,
        bio = doctor_data.bio,
        certificat_url = doctor_data.certificat_url,
        is_verified = False
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor

def get_doctor_by_slug(db:Session , slug : str) -> Doctor | None:
    return db.exec(select(Doctor).where(Doctor.slug == slug)).first()

def activate_doctor(db: Session, slug: str) -> User| None:
    # Récupère le docteur
    doctor = get_doctor_by_slug(db, slug)
    if not doctor:
        return False

    # Active le compte utilisateur lié
    user = db.exec(select(User).where(User.slug == doctor.user_slug)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    if user.is_active:
        raise HTTPException(status_code=400, detail="Ce compte est déjà activé.")

    # Activation
    user.is_active = True
    db.commit()
    db.refresh(user)

    # Marque le docteur comme vérifié
    doctor.is_verified = True
    db.refresh(doctor)

    # Enregistre les modifications
    db.commit()

    html_body = f""" 
    <p>Bonjour {user.first_name},</p>
    <p>Votre compte a été <strong>activé</strong> avec succès 🎉.</p>
    <p>Vous pouvez maintenant vous connecter à MedicalApp.</p>
    <p><a href='https://votre-site.com/login'>Se connecter</a></p>
    <p> Merci & Bienvenue 😊 </p>
    """
    send_email(
        subject= "Activation de votre compte sur MedicalApp",
        to = user.email,
        body= html_body
    )
    return doctor



def list_doctors(db: Session) -> list[Doctor]:
    return db.exec(select(Doctor)).all()

def update_doctor(db: Session, slug: str, updates: DoctorUpdate) -> Doctor:
    doctor = get_doctor_by_slug(db, slug)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    user = get_user_by_slug(db , doctor.user_slug)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update User
    user_data = updates.dict(exclude_unset=True, include={
        "first_name", "last_name", "email", "phone", "address", "birth_date", "sex", "password"
    })
    if "password" in user_data:
        user_data["password"] = hash_password(user_data["password"])
    for key, value in user_data.items():
        setattr(user, key, value)

    # Update Doctor
    doctor_data = updates.dict(exclude_unset=True, exclude=user_data.keys())
    for key, value in doctor_data.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)
    return doctor
 



def delete_doctor(db: Session, slug : str) -> bool : 
    doctor = get_doctor_by_slug(db, slug)
    if doctor: 
        db.delete(doctor)
        db.commit()
        return True
    return False