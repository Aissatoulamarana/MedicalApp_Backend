from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from typing import Optional , TYPE_CHECKING
from uuid import uuid4
from datetime import datetime, date
from enum import Enum

if TYPE_CHECKING:
    from app.doctor.models import Doctor

class SexEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class RoleEnum(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    slug: str = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(String(36), unique=True, nullable=False , index=True,),
    )

    first_name: str = Field(sa_column=Column(String(100), nullable=False))
    last_name: str = Field(sa_column=Column(String(100), nullable=False))

    email: str = Field(
        sa_column=Column(String(255), unique=True, index=True, nullable=False)
    )

    phone: str = Field(sa_column=Column(String(20), nullable=False))

    birth_date: date = Field(sa_column=Column(DateTime, nullable=False))

    sex: Optional[SexEnum] = Field(default=None, sa_column=Column(String(10)))
    address: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    role: Optional[RoleEnum] = Field(default=None, sa_column=Column(String(20)))

    password: str = Field(sa_column=Column(String(255), nullable=False))

    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    date_joined: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    doctor : Optional["Doctor"] = Relationship(back_populates = "user")
