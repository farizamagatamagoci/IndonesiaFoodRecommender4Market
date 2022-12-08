from fastapi.exceptions import HTTPException
import sqlalchemy as sa
from sqlalchemy.orm import Session

from app.models.transaction import Transaction

from app.utils.db import db_engine

from fastapi import Depends
from app.dependencies.authentication import Authentication

async def transaction_cancel(transaction_id: int, payload = Depends(Authentication())):
    with Session(db_engine) as session:
        transaction = session.query(
            Transaction
        ).filter(
            Transaction.id == transaction_id
        ).first()

        if not transaction:
            raise HTTPException(404, detail='Transaksi tidak ditemukan')
        
        total = transaction.price * (transaction.qty * -1)

        new_transaction = Transaction(
            transaction_id=transaction.transaction_id,
            food_id=transaction.food_id,
            food_name=transaction.food_name,
            price=transaction.price,
            qty=transaction.qty * -1,
            total=total
        )

        session.add(new_transaction)

        session.execute(
            sa.update(
                Transaction
            ).values(
                total=Transaction.total + total
            ).where(
                Transaction.id == transaction.transaction_id
            )
        )

        session.commit()