from sqlmodel import Session, select
from .models import Hospital
from .schemas import HospitalCreate , HospitalUpdate
from app.utils.geolocation import get_coordinates
from fastapi import HTTPException

def create_hospital(db: Session , hospital_data : HospitalCreate) -> Hospital:
    coords = get_coordinates(hospital_data.address)
    if not coords:
        raise HTTPException(status_code =400, detail = 'Adresse invalide ou non localisable ')
    
    hospital = Hospital(
        name = hospital_data.name,
        address = hospital_data.address,
        latitude = coords[0],
        longitude = coords[1],
        phone = hospital_data.phone,
        email = hospital_data.email,
        image_url = hospital_data.image_url

    )
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    return hospital

def get_hospital_by_slug(db : Session, slug : str) -> Hospital | None:
    hospital = db.exec(select(Hospital).where(Hospital.slug == slug)).first()
    return hospital

def existing_hospital(db : Session , name : str) -> Hospital | None:
    db.exec(select(Hospital).where(Hospital.name == name))

def list_hospitals(db: Session) -> list[Hospital]:
    return db.exec(select(Hospital)).all()

def update_hospital(db : Session, slug : str , hospital_update : HospitalUpdate ) -> Hospital | None:
    hospital = get_hospital_by_slug(db, slug)
    if hospital:
        update_data = hospital_update.dict(exclude_unset = True)
        for key , value in update_data.items():
            setattr(hospital , key , value)
        db.commit()
        db.refresh(hospital)
        return(hospital)
    return None

def delete_hospital(db : Session , slug :str) -> bool :
    hospital = get_hospital_by_slug(db, slug)
    if hospital:
        db.delete(hospital)
        db.commit()
        return True
    return False