import sqlalchemy as sa
from pydantic import BaseModel
from fastapi import Depends, Response
from fastapi.exceptions import HTTPException
from werkzeug.security import check_password_hash

from server.models.user import User
from server.models.user_login import UserLogin
from server.auth.get_db_session import get_db_session
from server.config import config
from server.utils.generate_access_token import generate_access_token

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

    user_login = UserLogin(
        user_id = user.id,
        expired_at = sa.func.NOW() + config.ACCESS_TOKEN_EXPIRATION
    )  

    session.add(user_login)
    session.commit()

    access_token, access_token_expired_at = generate_access_token(payload)

    return {
        "User ID": user.id,
        "Access token":access_token,
        "Expired at":access_token_expired_at
    }