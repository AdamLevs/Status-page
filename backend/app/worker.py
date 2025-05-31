import os
import time
import requests
import socket
import dns.resolver
import asyncio
import aiohttp
from celery import Celery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from .models import Service, HealthCheck
from .config import settings

# Celery
celery = Celery('worker', broker=settings.REDIS_URL)

# Database
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


# Entry point - periodic task
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


# Dispatcher
def perform_check(service):
    try:
        start = time.time()
        if service.check_type == "HTTP":
            response = requests.get(service.check_target, timeout=10)
            response_time = time.time() - start
            return ("UP" if response.status_code == 200 else "DOWN", response_time, None)

        elif service.check_type == "PING":
            return ping_check(service.check_target)

        elif service.check_type == "TCP":
            return tcp_check(service.check_target)

        elif service.check_type == "DNS":
            return dns_check(service.check_target)

        else:
            return ("UNKNOWN", 0, "Unsupported check type")
    except Exception as e:
        return ("DOWN", 0, str(e))


# PING CHECK
def ping_check(host):
    response = os.system(f"ping -c 1 {host} > /dev/null 2>&1")
    return ("UP" if response == 0 else "DOWN", 0, None if response == 0 else "Ping failed")


# TCP CHECK
def tcp_check(target):
    try:
        host, port = target.split(":")
        port = int(port)
        with socket.create_connection((host, port), timeout=5):
            return ("UP", 0, None)
    except Exception as e:
        return ("DOWN", 0, str(e))


# DNS CHECK
def dns_check(domain):
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return ("UP", 0, None)
    except Exception as e:
        return ("DOWN", 0, str(e))
