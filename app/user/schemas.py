from pydantic import BaseModel, EmailStr , Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_date: date
    sex: Optional[str] = None
    address: Optional[str] = None
    role: Optional[str] = None
   

class UserCreate(UserBase):
    password: str = Field(min_length = 6)

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    address: Optional[str] = None
    

class UserUpdatePassword(BaseModel):
    email : EmailStr
    password : str

class UserRead(UserBase):
    slug : UUID
    is_active : bool
    date_joined : datetime

    class Config:
        orm_mode = True

 