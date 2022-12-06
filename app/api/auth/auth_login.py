import time
from datetime import datetime, timedelta
import sqlalchemy as sa
from pydantic import BaseModel
from fastapi import Depends, Response
from fastapi.exceptions import HTTPException
from werkzeug.security import check_password_hash

import os

from app.models.user import User
from app.models.user_login import UserLogin
from app.dependencies.get_db_session import get_db_session
from app.config import config
from app.utils.generate_refresh_token import generate_refresh_token
from app.utils.generate_access_token import generate_access_token

class loginData(BaseModel):
    username: str
    password :str


async def auth_login(data: loginData, session = Depends(get_db_session)):
    #check username valid atau nggak
    user = session.execute(
        sa.select(
            User.id,
            User.password
        ).where(
            User.username== data.username
        )
    ).fetchone()

    if not user or not check_password_hash(user.password, data.password):
        raise HTTPException(400, detail = 'Username/password tidak cocok') #sangat secure karena user gatau password atau username yang salah

    payload = {
        'uid': user.id,
        'username': data.username
    }

    refresh_token = generate_refresh_token(payload)

    user_login = UserLogin(
        user_id = user.id,
        refresh_token = refresh_token,
        expired_at = sa.func.NOW() + config.REFRESH_TOKEN_EXPIRATION
    )  

    session.add(user_login)
    session.commit()

    access_token, access_token_expired_at = generate_access_token(payload)

    return {
        "User ID": user.id,
        "Access token":access_token,
        "Refresh token":refresh_token,
        "Expired at":access_token_expired_at
    }