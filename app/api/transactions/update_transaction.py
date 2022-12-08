from fastapi.exceptions import HTTPException
import sqlalchemy as sa
from sqlalchemy.orm import Session
from pydantic.main import BaseModel

from app.models.transaction import Transaction, TransactionStatus
from app.utils.db import db_engine

from fastapi import Depends
from app.dependencies.authentication import Authentication


class UpdateTransactionModel(BaseModel):
    status: int


async def transaction_update(transaction_id: int, data: UpdateTransactionModel, payload = Depends(Authentication())):
    with Session(db_engine) as session:
        transaction = session.query(
            Transaction
        ).filter(
            Transaction.id == transaction_id
        ).first()

        if not transaction:
            raise HTTPException(400, detail='Transaksi tidak ditemukan')
        
        if transaction.status >= TransactionStatus.COMPLETE:
            raise HTTPException(400, detail='Transaksi sudah sukses, tidak dapat diubah lagi')

        transaction.status = data.status

        session.add(transaction)
        session.commit()