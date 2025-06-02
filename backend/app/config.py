import os
from dotenv import load_dotenv


load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "Admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "statuspage")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
