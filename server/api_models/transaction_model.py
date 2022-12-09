from datetime import datetime
from pydantic import BaseModel

class TransactionModel(BaseModel):
    transaction_id: int
    created_at: datetime
    food_id: int
    food_name: str
    price: int
    qty: int
    total: int
    status: int