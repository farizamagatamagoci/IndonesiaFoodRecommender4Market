from sqlalchemy.orm import sessionmaker
from server.utils.db import db_engine
from typing import Optional
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