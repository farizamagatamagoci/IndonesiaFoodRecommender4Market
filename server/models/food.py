import sqlalchemy as sa
from server.models import Base


class Food(Base):
    __tablename__ = 'Food'

    id = sa.Column('id', sa.Integer, primary_key=True)
    barcode = sa.Column('barcode', sa.String)
    name = sa.Column('name', sa.String)
    price = sa.Column('price', sa.Integer)
    is_active = sa.Column('is_active', sa.Integer)
    created_at = sa.Column('created_at', sa.DateTime)
    modified_at = sa.Column('modified_at', sa.DateTime)