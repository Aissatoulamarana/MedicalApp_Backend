from fastapi import APIRouter , Depends , HTTPException, status
from sqlmodel import Session
from . import crud , schemas
from app.core.database import get_session as get_db


router = APIRouter(prefix = "/hospital" , tags=["hospital"])

@router.post("/", response_model=schemas.HospitalRead)
def create_hospital(hospital_data: schemas.HospitalCreate, db: Session = Depends(get_db)):
    existing = crud.existing_hospital(db , hospital_data.name)
    if existing : 
        raise HTTPException(status_code=400, detail="Un hôpital avec ce nom existe déjà")

    hospital = crud.create_hospital(db, hospital_data)

    maps_url = None
    if hospital.latitude and hospital.longitude:
        maps_url = f"https://www.google.com/maps?q={hospital.latitude},{hospital.longitude}"

    return {
        **hospital.dict(),
        "maps_url": maps_url
    }


@router.get("/{slug}", response_model = schemas.HospitalRead )
def read_hospital(slug : str , db: Session = Depends(get_db)):
    hospital = crud.get_hospital_by_slug(db, slug)
    if not hospital:
        raise HTTPException(status_code = 404 , detail = "Cet hôpital est introuvable")
    
    return hospital

@router.get("/" , response_model = list[schemas.HospitalRead])
def list_hospitals(db : Session = Depends(get_db)):
    return crud.list_hospitals(db)

@router.patch("/{slug}" , response_model = schemas.HospitalRead)
def update_hospital(slug: str, updates: schemas.HospitalUpdate, db: Session= Depends(get_db)):
    hospital = crud.update_hospital(db, slug, updates)
    if not hospital:
        raise HTTPException(status_code = 404 , detail = "Hôpital Non trouvé")
    return hospital

@router.delete('/{slug}')
def delete_hospital(slug : str, db : Session = Depends(get_db)):
    success = crud.delete_hospital(db, slug)
    if not success:
        raise HTTPException(status_code = 400 , detail = 'Suppression echouée')
    return {"Hôpital supprimé avec succès"}