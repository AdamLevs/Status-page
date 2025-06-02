from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import config

engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()