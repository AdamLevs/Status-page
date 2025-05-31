import os
import requests
import time
from celery import Celery
from celery.schedules import crontab
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Service, HealthCheck
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")

celery = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# הגדרת Beat: תריץ את המשימה כל דקה
celery.conf.beat_schedule = {
    "check-services-every-minute": {
        "task": "app.worker.check_services",
        "schedule": crontab(minute="*/1"),
    },
}

celery.conf.timezone = 'UTC'

@celery.task
def check_services():
    db = SessionLocal()
    services = db.query(Service).filter(Service.is_active == True).all()

    for service in services:
        try:
            start = time.time()
            if service.check_type == "HTTP":
                response = requests.get(service.check_target, timeout=10)
                response_time = time.time() - start
                status = "UP" if response.status_code == 200 else "DOWN"
                error = None
            else:
                status = "SKIPPED"
                response_time = 0
                error = "Check type not supported yet"
        except Exception as e:
            status = "DOWN"
            response_time = 0
            error = str(e)

        hc = HealthCheck(
            service_id=service.id,
            status=status,
            response_time=response_time,
            error_message=error
        )
        db.add(hc)
        service.last_checked_at = datetime.utcnow()
        db.commit()

    db.close()