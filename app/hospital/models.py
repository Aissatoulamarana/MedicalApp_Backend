from sqlmodel import SQLModel , Field , Relationship
from sqlalchemy import Column, String , DateTime
from typing import Optional , TYPE_CHECKING , List
from datetime import datetime
from uuid import uuid4

if TYPE_CHECKING:
    from app.doctor.models import Doctor

class Hospital(SQLModel, table=True ):
    id : Optional[int] = Field(default = None, primary_key = True)

    slug : str = Field(
        default_factory = lambda: str(uuid4()),
        sa_column = Column(String(36), unique=  True, nullable = False, index = True)
    )

    name : str = Field(sa_column = Column(String(100), nullable = False))
    address: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    email: str = Field(
        sa_column=Column(String(255), unique=True, index=True, nullable=False)
    )
    phone: str = Field(sa_column=Column(String(20), nullable=False))
    latitude : Optional[float]
    longitude : Optional[float]
    image_url : Optional[str]
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    
    doctors : List["Doctor"] = Relationship(back_populates = "hospital")