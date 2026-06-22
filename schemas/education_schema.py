from pydantic import BaseModel
from typing import Optional

class Education(BaseModel):
    degree: str
    college_name: str
    specialization: str
    passing_year: int
    percentage: float


class UpdateEducation(BaseModel):
    degree: Optional[str] = None
    college_name: Optional[str] = None
    specialization: Optional[str] = None
    passing_year: Optional[int] = None
    percentage: Optional[float] = None