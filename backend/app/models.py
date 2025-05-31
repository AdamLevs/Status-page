from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from .database import Base
from datetime import datetime

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    check_type = Column(String)
    check_target = Column(String)
    frequency = Column(Integer)
    is_active = Column(Boolean, default=True)
    last_checked_at = Column(DateTime, nullable=True)

class HealthCheck(Base):
    __tablename__ = "healthchecks"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer)
    status = Column(String)
    response_time = Column(Float)
    error_message = Column(String, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow)
