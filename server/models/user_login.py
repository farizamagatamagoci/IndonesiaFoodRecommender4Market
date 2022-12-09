# bikin tabel user_login
import sqlalchemy as sa

from server.models import Base

import time
from datetime import datetime, timedelta
from typing import Optional

class UserLogin(Base):
    __tablename__ = 'UserLogin'

    id = sa.Column('id', sa.Integer, primary_key= True)
    user_id=sa.Column('user_id', sa.Integer, default=0)
    refresh_token=sa.Column('refresh_token', sa.String)
    expired_at = sa.Column('expired_at', sa.DateTime, default=sa.func.NOW())
    created_at = sa.Column('created_at', sa.DateTime, default=sa.func.NOW())
    modified_at = sa.Column('modified_at', sa.DateTime, default=sa.func.NOW(), onupdate=sa.func.NOW())