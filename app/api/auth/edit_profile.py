from app.dependencies.authentication import Authentication
from app.dependencies.get_db_session import get_db_session
from app.models.user import User
from werkzeug.security import generate_password_hash

from typing import Optional
from pydantic import BaseModel, root_validator
from fastapi import Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

import sqlalchemy as sa

class EditProfileData(BaseModel):
    username: Optional[str]
    full_name: Optional[str]
    password: Optional[str]
    confirm_password: Optional[str]

    @root_validator
    def validate_confirm_password(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')

        if password and confirm_password != password:
            raise ValueError('Confirm password tidak cocok')

        return values


async def edit_profile(data: EditProfileData, payload= Depends(Authentication), session = Depends(get_db_session)):
    profile_data = jsonable_encoder(data)

    user_id = payload.get('uid',0)

    if 'username' in profile_data and profile_data['username']:
        #checkusername exist
        check_username = session.execute(
            sa.select(User.id).where
                (sa.and_(
                    User.username == profile_data['username'],
                    User.id != user_id
                )
            )
        ).fetchone()

        if check_username:
            raise HTTPException(400, 'Username sudah digunakan')

        values_to_update.update({
            'username': profile_data['username']
        })
    
    if 'full_name' in profile_data and profile_data['full_name']:
        values_to_update.update({
            'full_name': profile_data['full_name']
        })
    
    if 'password' in profile_data and profile_data['password']:
        password = generate_password_hash(profile_data['password'])
        values_to_update.update({'password': password})

    values_to_update= {} #adalah fill fill yang akan diupdate 

    result = session.execute(
        sa.update(User).values(**values_to_update).where(User.id == user_id)
    )
    if result.rowcount == 0: #artinya gaada user yang valid
        raise HTTPException(400, detail= 'User tidak ditemukan')

    session.commit()
    return Response(status_code=204)