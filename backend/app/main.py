from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from app import models, database, crud, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running!"}

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/services", response_model=schemas.ServiceOut)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    valid_check_types = ("HTTP", "PING", "TCP", "DNS", "SSH")
    if service.check_type not in valid_check_types:
        raise HTTPException(status_code=400, detail=f"Invalid check type. Valid options: {valid_check_types}")
    return crud.create_service(db, service)

@app.get("/services", response_model=list[schemas.ServiceOut])
def read_services(db: Session = Depends(get_db)):
    return crud.get_services(db)

@app.get("/services/{service_id}/health", response_model=list[schemas.HealthCheckOut])
def read_health(service_id: int, db: Session = Depends(get_db)):
    service = crud.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return crud.get_health_checks(db, service_id)

@app.get("/public")
def public_status(db: Session = Depends(get_db)):
    services = db.query(models.Service).options(joinedload(models.Service.health_checks)).all()
    result = []
    now = datetime.utcnow()
    staleness_limit = timedelta(minutes=5)

    for s in services:
        healths = s.health_checks or []
        last_health = max(
            (h for h in healths if h.checked_at is not None),
            key=lambda x: x.checked_at,
            default=None
        ) if healths else None

        if last_health:
            age = now - last_health.checked_at
            if age > staleness_limit:
                status = "Unknown"
            else:
                status = last_health.status
        else:
            status = "Unknown"

        result.append({
            "name": s.name,
            "status": status,
            "last_checked_at": last_health.checked_at.isoformat() if last_health else None,
            "response_time": last_health.response_time if last_health else None,
            "error_message": last_health.error_message if last_health else None
        })

    return result

@app.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    success = crud.delete_service(db, service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}