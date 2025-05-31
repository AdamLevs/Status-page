import os
import secrets
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from app.models import Base, User
from passlib.hash import bcrypt


load_dotenv()

POSTGRES_USER = "Admin"
POSTGRES_PASSWORD = "Password"
POSTGRES_DB = "statuspage"
POSTGRES_PORT = "55432"
POSTGRES_HOST = "db"
REDIS_HOST = "redis"
REDIS_PORT = "6379"
REDIS_DB = "0"
SECRET_KEY = secrets.token_urlsafe(32)

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")

with open(env_path, "w") as f:
    f.write(f"POSTGRES_USER={POSTGRES_USER}\n")
    f.write(f"POSTGRES_PASSWORD={POSTGRES_PASSWORD}\n")
    f.write(f"POSTGRES_DB={POSTGRES_DB}\n")
    f.write(f"POSTGRES_HOST={POSTGRES_HOST}\n")
    f.write(f"POSTGRES_PORT={POSTGRES_PORT}\n")
    f.write(f"REDIS_HOST={REDIS_HOST}\n")
    f.write(f"REDIS_PORT={REDIS_PORT}\n")
    f.write(f"REDIS_DB={REDIS_DB}\n")
    f.write(f"DATABASE_URL=postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}\n")
    f.write(f"REDIS_URL=redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}\n")
    f.write(f"SECRET_KEY={SECRET_KEY}\n")
    f.write(f"RUNNING_IN_DOCKER=true\n")

print("✅ .env file generated successfully.")

def create_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{POSTGRES_DB}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {POSTGRES_DB}")
            print(f"✅ Database '{POSTGRES_DB}' created.")
        else:
            print(f"ℹ️ Database '{POSTGRES_DB}' already exists.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error creating database: {e}")

create_database()

load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")

def create_default_admin():
    db = SessionLocal()
    admin_email = "admin@admin.com"
    existing_admin = db.query(User).filter_by(email=admin_email).first()
    if not existing_admin:
        admin_user = User(
            email=admin_email,
            hashed_password=bcrypt.hash("Password"),
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print("✅ Admin user created.")
    else:
        print("ℹ️ Admin user already exists.")
    db.close()

create_default_admin()
