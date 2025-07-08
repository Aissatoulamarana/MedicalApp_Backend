from pydantic import BaseModel, EmailStr , Field
from typing import Optional
from uuid import UUID
from datetime import datetime , date
from enum import Enum
from app.user.schemas import UserRead , UserUpdate
from app.hospital.schemas import HospitalRead


class SexEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class DoctorCreate(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    phone : str
    birth_date : date
    address: Optional[str] = None
    password : str
    sex : Optional[SexEnum]

    hospital_slug : str
    speciality : Optional[str]
    bio : Optional[str]
    certificat_url : str

class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    address: Optional[str] = None
    speciality : Optional[str] = None
    bio : Optional[str] = None


class DoctorRead(BaseModel):
    id : int
    slug : UUID
    user : UserRead
    hospital : HospitalRead
    speciality : Optional[str]
    bio : Optional[str]
    certificat_url : Optional[str]
    is_verified : bool
    user_slug : str
    hospital_slug : str

    class Config:
        orm_mode = True