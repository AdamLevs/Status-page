from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, UniqueConstraint
from app.database import Base
from datetime import datetime

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    check_type = Column(String(20), nullable=False)
    check_target = Column(String(255), nullable=False)
    frequency = Column(Integer, nullable=False, default=60)
    is_active = Column(Boolean, default=True)
    last_checked_at = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint('name', 'check_target', name='unique_service_name_target'),
    )


class HealthCheck(Base):
    __tablename__ = "healthchecks"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    status = Column(String(10), nullable=False)
    response_time = Column(Float, nullable=True)
    error_message = Column(String(255), nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
