import time
from typing import Tuple
from app.config import config

import jwt

def generate_access_token(payload: str) -> Tuple[str, int]:
    current_time = int(time.time())
    expired_at = current_time + config.ACCESS_TOKEN_EXPIRATION

    payload.update({
        'exp' : expired_at,
        'iat' : current_time
    })

    access_token = jwt.encode(payload, config.PRIVATE_KEY.encode('utf-8'), 'RS256')

    return access_token, expired_at

# BERHASIL
# generate_access_token(payload)
# ('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjEwMDAsImV4cCI6MTY2OTU5OTA4MSwiaWF0IjoxNjY5NTk4NzgxfQ.Gu2QRKEyVF3o_cD74Z8k5Laflq1oypI9j9OkuuqjfE07tp0hVy7nQbsaXV4Iff85Va68FaEKf7x_g7BlWRBxDRfYHMqwDyhJmGjlOUgVxpS8EeITrbjbU-pVNGBUm4FbuMkI6CEracdjpGEhsOB_hnn03zkdmJFvO6zMh4R7qPbOnJXDZeVNlCxmQIAmZZreMXZSYvGH_ymXacPJBYGlbwTvMzIU8VK0uSK00timId22RMjSwg8CK4QuVSu-uBn-IVcQHpUjeCthVLs26SVPkq9IZH-vM17QmyMJh4Nk0CAD-s7eRRmk8hN3QTk_4bVdRZ2C9e-16j4X5rKlifmXQw', 1669599081)