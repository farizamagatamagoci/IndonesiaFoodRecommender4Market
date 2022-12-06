from fastapi import Depends
import sqlalchemy as sa

from app.api_models.base_response import BaseResponseModel
from app.dependencies.authentication import Authentication
from app.dependencies.get_db_session import get_db_session
from app.models.user import User
from app.api_models.profile_model import ProfileModel

class GetProfileResponseModel(BaseResponseModel):
    data: ProfileModel

    class config:
        schema_extra = {
            'example': {
                'data' : {
                    'id' : 1000,
                    'username' : 'mfarizram18',
                    'full_name' : 'M Fariz R',
                },
                'meta': {},
                'message': 'Success',
                'success' : True,
                'code' : 200
            }
        }

async def get_profile(payload = Depends(Authentication()), session = Depends(get_db_session)):
    user_id = payload('uid', 0)
    profile = session.execute(
        sa.select(
            User.id,
            User.username,
            User.full_name
        ).where(
            User.id == user_id
        )
    ).fetchone() #kalau internal error

    return GetProfileResponseModel(
        data = ProfileModel(
            id = profile.id,
            username= profile.username,
            full_name= profile.username
        )
    )

