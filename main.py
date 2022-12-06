from fastapi import FastAPI
import uvicorn
from app.models import user
from app.models import user_login
from app.api import api_router
from app.utils.db import db_engine

from app import *

user.Base.metadata.create_all(db_engine)
user_login.Base.metadata.create_all(db_engine)

@app.get('/')
def index():
    return {"18220081 - M Fariz Ramadhan" : "Halo Pendakick!"}