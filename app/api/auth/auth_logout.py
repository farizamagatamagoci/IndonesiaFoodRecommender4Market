from pydantic import BaseModel
from fastapi import Depends,Response
from fastapi.exceptions import HTTPException

import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.models.user_login import UserLogin

class LogOutData(BaseModel):
    refresh_token: str

async def auth_logout(data: LogOutData, session= Depends(get_db_session)):
    result = session.execute(
        sa.delete(UserLogin).where(UserLogin.refresh_token == data.refresh_token)
    )

    if result.rowcount == 0:
        raise HTTPException(400,'Refresh token tidak ditemukan' )

    session.commit()
    
    return Response(status_code=204)