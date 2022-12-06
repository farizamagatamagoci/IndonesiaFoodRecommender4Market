from sqlalchemy import create_engine

from app.config import config

SQLALCHEMY_DATABASE_URL = 'sqlite:///./userpendakick'

db_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {"check_same_thread": False},
    echo=True
)

# db_engine = sa.create_engine(
#     config.DB,
#     pool_pre_ping= config.DB_POOL_PRE_PING,
#     pool_size=config.DB_POOL_SIZE,
#     pool_recycle=config.DB_POOL_RECYCLE,
#     echo=config.DB_ECHO
# )