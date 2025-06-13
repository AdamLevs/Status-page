from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from app import models, database, crud, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/")
def root_message():
    return {"message": "API is running!"}

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/services", response_model=schemas.ServiceOut)
def create_monitoring_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    valid_check_types = ("HTTP", "PING", "TCP", "DNS", "SSH")
    if service.check_type not in valid_check_types:
        raise HTTPException(status_code=400, detail=f"Invalid check type. Valid options: {valid_check_types}")
    return crud.create_service(db, service)

@app.get("/services", response_model=list[schemas.ServiceOut])
def list_all_services(db: Session = Depends(get_db)):
    return crud.get_services(db)

@app.get("/services/{service_id}/stats")
def get_latest_server_stats(service_id: int, db: Session = Depends(get_db)):
    stats = crud.get_latest_stats(db, service_id)
    if not stats:
        raise HTTPException(status_code=404, detail="No stats found")
    return {
        "cpu_usage": stats.cpu_usage,
        "memory_usage": stats.memory_usage,
        "disk_usage": stats.disk_usage,
        "created_at": stats.created_at
    }

@app.get("/services/{service_id}/health", response_model=list[schemas.HealthCheckOut])
def get_service_health_checks(service_id: int, db: Session = Depends(get_db)):
    service = crud.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return crud.get_health_checks(db, service_id)

@app.get("/public")
def get_public_status_view(db: Session = Depends(get_db)):
    services = db.query(models.Service).options(joinedload(models.Service.health_checks)).all()
    result = []
    now = datetime.utcnow()
    staleness_limit = timedelta(minutes=5)

    for service in services:
        health_checks = service.health_checks or []
        last_check = max(
            (h for h in health_checks if h.checked_at),
            key=lambda x: x.checked_at,
            default=None
        ) if health_checks else None

        if last_check:
            age = now - last_check.checked_at
            status = "Unknown" if age > staleness_limit else last_check.status
        else:
            status = "Unknown"
        result.append({
            "name": service.name,
            "status": status,
            "last_checked_at": last_check.checked_at.isoformat() if last_check else None,
            "response_time": last_check.response_time if last_check else None,
            "error_message": last_check.error_message if last_check else None
        })
    return result

@app.delete("/services/{service_id}")
def delete_monitoring_service(service_id: int, db: Session = Depends(get_db)):
    try:
        success = crud.delete_service(db, service_id)
        if not success:
            raise HTTPException(status_code=404, detail="Service not found")
        return {"message": "Service deleted successfully"}
    except Exception as e:
        print(f"[Delete Error] {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")