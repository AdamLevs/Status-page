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
