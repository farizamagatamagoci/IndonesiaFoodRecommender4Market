import jwt
from app.config import config

def get_payload(access_token: str, verify_exp: bool = True) -> dict:
     # ini verify_exp -> True biar dicek, kalau mau false berarti ga dicek
    payload = jwt.decode(access_token, config.PUBLIC_KEY, ['RS256'], options= {'verify_exp': verify_exp})

    return payload


#berguna ketika melihat access token yang sudah expired
#refresh token gabisa dipake karena beda verificationnyanya