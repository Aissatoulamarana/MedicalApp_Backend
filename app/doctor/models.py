from sqlmodel import SQLModel, Field , Relationship
from sqlalchemy import Column, String , DateTime
from typing import Optional
from uuid import uuid4 , UUID
from datetime import datetime
from app.user.models import User
from app.hospital.models import Hospital


class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    slug: str = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(String(36), unique=True, nullable=False , index=True,),
    )

    user_slug: str = Field(foreign_key="user.slug")
    user : Optional["User"] = Relationship(back_populates='doctor')

    hospital_slug: str = Field(foreign_key="hospital.slug")
    hospital : Optional["Hospital"] = Relationship(back_populates='doctors')

    speciality: Optional[str]
    bio : Optional[str]
    certificat_url : Optional[str]
    is_verified : bool = Field(default=False)

    date_joined: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )