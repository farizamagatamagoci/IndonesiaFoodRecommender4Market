from fastapi import FastAPI
from app.models import user
from app.models import user_login
from app.utils.db import db_engine

from fastapi import Response
from http import HTTPStatus

from app import *

user.Base.metadata.create_all(db_engine)
user_login.Base.metadata.create_all(db_engine)

@app.get('/')
def index():
    return {"18220081 - M Fariz Ramadhan" : "Halo Pembeli Kantin Burjo!"}
