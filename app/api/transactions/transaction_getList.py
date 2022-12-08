import sqlalchemy as sa
from sqlalchemy.orm import Session

from app.api_models.base_response import BaseResponseModel
from app.api_models.transaction_model import TransactionModel
from app.models.transaction import Transaction
from app.utils.db import db_engine

from fastapi import Depends
from app.dependencies.authentication import Authentication


class GetTransactionListResponseModel(BaseResponseModel):
    class Config:
        schema_extra = {
            'example': {
                'data': [
                    {
                    'id': 1,
                    'created_at': '2021-11-06 13:25',
                    'status': 10,
                    'total': 400
                    }
                ],
                'meta': {},
                'success': True,
                'code': 200,
                'message': 'Success'
            }
        }


async def transaction_getList(payload = Depends(Authentication())):
    with Session(db_engine) as session:
        transaction_list = session.query(
            Transaction
        ).order_by(
            sa.desc(Transaction.id)
        ).all()

        result = []

        for transaction in transaction_list:
            result.append(
                TransactionModel(
                    transaction_id=transaction.id,
                    created_at=transaction.created_at,
                    food_id= transaction.food_id,
                    food_name= transaction.food_name,
                    price= transaction.price,
                    qty = transaction.qty,
                    total=transaction.total,
                    status=transaction.status
                )
            )

        return GetTransactionListResponseModel(
            data=result
        )
