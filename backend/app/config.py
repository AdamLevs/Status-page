import os

class Settings:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin123")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "statuspage")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

settings = Settings()
