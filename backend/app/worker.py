import time
import requests
import socket
import dns.resolver
import subprocess
import ipaddress
from urllib.parse import urlparse
from celery import Celery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from app.models import Service, HealthCheck
import app.config as config

celery = Celery('worker', broker=config.REDIS_URL)
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def is_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def is_url(address):
    try:
        parsed = urlparse(address)
        return parsed.scheme in ('http', 'https')
    except:
        return False

def perform_check(service):
    start = time.time()

    try:
        if is_url(service.check_target):
            try:
                resp = requests.get(service.check_target, timeout=5)
                response_time = time.time() - start
                return "UP" if resp.ok else "DOWN", response_time, None
            except Exception as e:
                return "DOWN", None, str(e)

        if service.check_type == "PING":
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '3', service.check_target],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            success = result.returncode == 0
            response_time = time.time() - start
            return "UP" if success else "DOWN", response_time, None if success else result.stderr.decode()

        elif service.check_type == "TCP":
            try:
                host, port = service.check_target.split(":")
                port = int(port)
                s = socket.create_connection((host, port), timeout=5)
                response_time = time.time() - start
                s.close()
                return "UP", response_time, None
            except Exception as e:
                return "DOWN", None, str(e)

        elif service.check_type == "DNS":
            try:
                dns.resolver.resolve(service.check_target)
                response_time = time.time() - start
                return "UP", response_time, None
            except Exception as e:
                return "DOWN", None, str(e)

        else:
            return "DOWN", None, "Unsupported check type"

    except Exception as e:
        return "DOWN", None, str(e)


@celery.task
def check_services():
    db = SessionLocal()
    services = db.query(Service).filter(Service.is_active == True).all()

    for service in services:
        status, response_time, error = perform_check(service)
        hc = HealthCheck(
            service_id=service.id,
            status=status,
            response_time=response_time,
            error_message=error,
            checked_at=datetime.utcnow()
        )
        db.add(hc)
        service.last_checked_at = datetime.utcnow()
        db.commit()
    db.close()

celery.conf.beat_schedule = {
    "check-every-minute": {
        "task": "app.worker.check_services",
        "schedule": 60.0,
    }
}