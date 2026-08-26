from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime

class HospitalCreate(BaseModel):
    name : str
    address : str
    phone : Optional[str]
    email : EmailStr
    image_url : Optional[str]


class HospitalUpdate(BaseModel):
    name : Optional[str] = None
    address : Optional[str] = None
    email : Optional[EmailStr] = None
    phone : Optional[str] = None
    latitude : Optional[float] = None
    longitude : Optional[float] = None


class HospitalRead(BaseModel):
    slug : UUID
    name : str
    address : str
    phone : Optional[str]
    email : EmailStr
    latitude : float
    longitude : float
    created_at : datetime
    image_url : Optional[str]
    maps_url : Optional[str] = None

  
    class Config:
        orm_mode = True

