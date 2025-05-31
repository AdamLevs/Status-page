from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/services", response_model=schemas.ServiceOut)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    if service.check_type not in ("HTTP", "PING", "TCP", "DNS"):
        raise HTTPException(status_code=400, detail="Invalid check type")
    return crud.create_service(db, service)

@app.get("/services", response_model=list[schemas.ServiceOut])
def read_services(db: Session = Depends(get_db)):
    return crud.get_services(db)

@app.get("/services/{service_id}/health")
def read_health(service_id: int, db: Session = Depends(get_db)):
    return crud.get_health_checks(db, service_id)

@app.get("/public")
def public_status(db: Session = Depends(get_db)):
    services = crud.get_services(db)
    return [{"name": s.name, "status": s.last_checked_at is not None} for s in services]
