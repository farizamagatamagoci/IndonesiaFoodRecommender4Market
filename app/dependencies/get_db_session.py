from sqlalchemy.orm import Session, sessionmaker
from app.utils.db import db_engine
from app.models import Base

from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseSettings

session = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)

def get_db_session():
    db = session()
    try:
        yield db
    finally:
        db.close()

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = "default"
    ALGORTIM: Optional[str] = "HS256"

    class Config:
        env_file = ".env"