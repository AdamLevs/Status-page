from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    check_type = Column(String)
    check_target = Column(String)
    frequency = Column(Integer)
    is_active = Column(Boolean, default=True)
    last_checked_at = Column(DateTime, nullable=True)

class HealthCheck(Base):
    __tablename__ = "healthchecks"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    status = Column(String)
    response_time = Column(Float)
    error_message = Column(String, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow)