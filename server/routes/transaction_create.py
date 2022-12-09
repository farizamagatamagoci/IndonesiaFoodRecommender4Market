from pydantic import BaseModel
from server.api_models.base_response import BaseResponseModel
from server.models.transaction import Transaction
from server.models.food import Food
from fastapi.exceptions import HTTPException

from fastapi import Depends
from server.auth.authentication import Authentication
from server.auth.get_db_session import get_db_session

class CreateTransactionData(BaseModel):
    food_id: int
    price: int
    qty: int

class CreateTransactionResponseModel(BaseResponseModel):
    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id': 1,
                    'url': '/api/v1/transactions/1'
                },
                'meta': {},
                'success': True,
                'code': 200,
                'message': 'Success'
            }
        }

async def transaction_create(data: CreateTransactionData, session = Depends(get_db_session), payload = Depends(Authentication())):
        # check makanan
        food = session.query(
            Food.id, Food.name
        ).filter(
            Food.id == data.food_id
        ).filter(
            Food.is_active
        ).first()

        if not food:
            raise HTTPException(400, detail='Makanan tidak ditemukan atau sedang habis')
  
        total = data.price * data.qty

        transaction = Transaction(
            # transaction_id=data.transaction_id,
            food_id=data.food_id,
            food_name=food.name,
            price=data.price,
            qty=data.qty,
            total=total
        )

        session.add(transaction)
        session.commit()

        return CreateTransactionResponseModel(
            data={
                'id': transaction.id,
                'url': f'/api/v1/transaction-items/{transaction.id}'
            }
        )