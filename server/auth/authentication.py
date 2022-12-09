# akan memusatkan logic2 disini : user ga mengirim token, user token expired
# jadi disetiap endpoint kita tinggal panggil2 dependenciesnya
import jwt
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException

from fastapi import Request
from typing import Optional

from server.utils.get_payload import get_payload

class Authentication(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        authorization = await super().__call__(request)

        # if not authorization.credentials:
        #     return() #jika user ga ngasih credentials maka payloadnya dictionary kosong

        try :
            payload = get_payload(authorization.credentials)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                401, 
                detail = {
                    'message' : 'Token kadaluarsa', #ngasih tau kadaluarsa biar minta lg
                    'code' : 40100
                }
            )
        except jwt.DecodeError:
            raise HTTPException(
                401, detail = {
                    'message' : 'Token salah', #ngasih tau kadaluarsa biar minta lg
                    'code' : 40101
                }
            )
        
        return payload