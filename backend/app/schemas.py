from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ServiceCreate(BaseModel):
    name: str
    check_type: str
    check_target: str
    frequency: int

class ServiceOut(ServiceCreate):
    id: int
    is_active: bool
    last_checked_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
