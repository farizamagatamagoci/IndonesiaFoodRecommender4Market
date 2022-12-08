from fastapi.exceptions import HTTPException
from fastapi import Depends
from pydantic import BaseModel
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.sql.expression import func, text

from app.api_models.base_response import BaseResponseModel
from app.models.user_login import UserLogin
from app.models.user import User
from app.utils.generate_access_token import generate_access_token
from app.dependencies.get_db_session import get_db_session
from app.config import config

class RefreshTokenData(BaseResponseModel):
    refresh_token: str

class RefreshTokenDataResponseModel(BaseModel):
    access_token: str
    expired_at : int

 #refresh token digunakan untuk me-generate access token yang baru, setelah access token kadaluarsa
class RefreshTokenResponseModel(BaseResponseModel):
    data: RefreshTokenDataResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data' : {
                    'user_id' : 1000,
                    'refresh_token' : 'asdfghjkl',
                    'access_token' : 'zxcvbnm',
                    'expired_at' : 1234
                },
                'meta': {},
                'message': 'Success',
                'success' : True,
                'code' : 200
            }
        }

async def auth_refresh_token(data: RefreshTokenData, session = Depends(get_db_session)):
    #check refresh token
    user_login = session.execute(
        sa.select(
            UserLogin.id,
            User.id.label('user_id'),
            User.username,
            # sa.func.if_(
            #     UserLogin.expired_at > sa.func.NOW(), 0, 1 #jika expired_at lebih dari 0 (gabakal expired)
            # ).label('expired')
            # sa.case
            #     WHEN UserLogin.expired_at > sa.func.NOW(), 0, 1
            #     THEN UserLogin.expired
            #     ELSE NULL
            # END AS expired
            str((UserLogin.expired_at).label('expired'))
        ).where(
            UserLogin.user_id == User.id,
            UserLogin.refresh_token == data.refresh_token
        )
    ).fetchone()

    if not user_login:
        raise HTTPException(400, detail= 'Refresh token tidak ditemukan')

    if user_login.expired:
        raise HTTPException(403, detail={
            'message': 'Refresh token kadaluarsa',
            'code' : 40301
            } 
        )
    
    # untuk memperpanjang refresh token
    session.execute(
        sa.update(UserLogin).values(expired_at = sa.func.NOW() + config.REFRESH_TOKEN_EXPIRATION)
    )

    #generate new access token
    #refresh token digunakan untuk me-generate access token yang baru, setelah access token kadaluarsa
    payload = {
        'uid' : user_login.user_id,
        'username' : user_login.username
    }

    access_token, expired_at = generate_access_token(payload)

    session.commit()

    return RefreshTokenResponseModel(
        data = RefreshTokenDataResponseModel(
            access_token= access_token,
            expired_at = expired_at
        )
    )

#auth profile nanti akan kita dapatkan dari jwt token