from pydantic import BaseModel
from datetime import date
from typing import Optional


class PersonalDetails(BaseModel):
    father_name: str
    mother_name: str
    date_of_birth: date
    marital_status: str
    nationality: str
    blood_group: str
    emergency_contact: int
    alternate_email: str


class UpdatePersonalDetails(BaseModel):
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    marital_status: Optional[str] = None
    nationality: Optional[str] = None
    blood_group: Optional[str] = None
    emergency_contact: Optional[int] = None
    alternate_email: Optional[str] = None