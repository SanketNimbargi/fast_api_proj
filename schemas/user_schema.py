from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    age: int
    phone: int
    gender: str
    address: str
    city: str
    state: str
    country: str
    pincode: int


class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[int] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[int] = None