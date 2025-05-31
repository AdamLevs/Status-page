import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

IN_DOCKER = os.getenv("RUNNING_IN_DOCKER", "false").lower() == "true"

DEFAULTS = {
    "POSTGRES_USER": "Admin",
    "POSTGRES_PASSWORD": "Password",
    "POSTGRES_DB": "statuspage",
    "POSTGRES_HOST_DOCKER": "db",
    "POSTGRES_HOST_LOCAL": "localhost",
    "POSTGRES_PORT": "5432"
}

POSTGRES_USER = os.getenv("POSTGRES_USER", DEFAULTS["POSTGRES_USER"])
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", DEFAULTS["POSTGRES_PASSWORD"])
POSTGRES_DB = os.getenv("POSTGRES_DB", DEFAULTS["POSTGRES_DB"])
POSTGRES_PORT = os.getenv("POSTGRES_PORT", DEFAULTS["POSTGRES_PORT"])

POSTGRES_HOST = (
    os.getenv("POSTGRES_HOST", DEFAULTS["POSTGRES_HOST_DOCKER" if IN_DOCKER else "POSTGRES_HOST_LOCAL"])
)

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

print(f"Using DB at {DATABASE_URL}")