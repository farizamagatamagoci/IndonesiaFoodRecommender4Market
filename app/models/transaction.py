import sqlalchemy as sa
from app.models import Base

class TransactionStatus:
    OUTSTANDING: int = 10
    COMPLETE: int = 20
    CANCELED: int = 30

class Transaction(Base):
    __tablename__ = 'Transaction'

    id = sa.Column('id', sa.Integer, primary_key=True)
    transaction_id = sa.Column('transaction_id', sa.Integer)
    created_at = sa.Column('created_at', sa.DateTime, default=sa.func.NOW())
    modified_at = sa.Column('modified_at', sa.DateTime, default=sa.func.NOW(), onupdate=sa.func.NOW())
    food_id = sa.Column('food_id', sa.Integer)
    food_name = sa.Column('food_name', sa.String)
    price = sa.Column('price', sa.Integer)
    qty = sa.Column('qty', sa.Integer)
    total = sa.Column('total', sa.Integer)
    status = sa.Column('status', sa.Integer, default=TransactionStatus.OUTSTANDING)