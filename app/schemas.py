from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

# Service schemas

class ServiceBase(BaseModel):
    name: str
    check_type: str
    check_target: str
    frequency: int

class ServiceCreate(ServiceBase):
    pass

class ServiceOut(ServiceBase):
    id: int
    is_active: bool
    last_checked_at: Optional[datetime]

    class Config:
        from_attributes = True

# Healthcheck schemas

class HealthCheckOut(BaseModel):
    id: int
    service_id: int
    status: str
    response_time: float
    error_message: Optional[str]
    checked_at: datetime

    class Config:
        from_attributes = True