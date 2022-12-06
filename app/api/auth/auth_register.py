from pydantic import BaseModel, root_validator
from fastapi import Response, Depends
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash

import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.models.user import User

class RegisterData(BaseModel):
    username: str
    full_name: str
    password : str
    confirm_password: str

    @root_validator
    def validate_confirm_password(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')

        if confirm_password != password:
            raise ValueError('Confirm Password tidak cocok')
        
        return values

async def auth_register(data: RegisterData, session = Depends(get_db_session)): #kekurangannya endpoint yang memiliki database akan memanggil dari awal, pas ga dibutuhin jg dipanggil
    # check if username already existed
    check_username = session.execute(
        sa.select(User.id).where(User.username == data.username)
    ).scalar()

    if check_username:
        raise HTTPException(400, detail ='Username sudah digunakan')

    encrypted_password = generate_password_hash(data.password)

    user = User(
        username = data.username,
        full_name = data.full_name,
        password = encrypted_password
    )

    session.add(user)
    session.commit()

    return Response(status_code= 201) # detail = 'User berhasil dibuat')

# JADI END POINT-NYA CATET
# end point register
# kalau success 201
# ada session commit yaitu dipanggil di get_db_session
# commitnya berjalan setelah response selesai
#data bener2 disimpan ketika end-pointnya sukses