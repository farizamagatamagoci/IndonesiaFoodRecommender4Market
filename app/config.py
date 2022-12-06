from pydantic import BaseSettings
from functools import lru_cache

class Config(BaseSettings):
    ACCESS_TOKEN_EXPIRATION: int = 5 * 60   # 5 menit
    REFRESH_TOKEN_EXPIRATION: int = 1* 24 * 60 * 60  # 1 hari +

    PRIVATE_KEY : str
    PUBLIC_KEY : str
    REFRESH_PRIVATE_KEY: str

    DB: str
    DB_POOL_PRE_PING : bool = True #setiap kali melakukan query ngeping dulu
    DB_POOL_SIZE : int = 20 #sqlalchemy membuat 20 conncection pool
    DB_POOL_RECYCLE: int = 1800 #setiap setengah jam connection2 pool nya di recycle, suka putus sendiri jadi harus direcycle
    DB_ECHO: bool = False #setiap query akan diunlock

    class Config:
        env_file = '.env'

@lru_cache
def get_config():
    return Config()

config = get_config()