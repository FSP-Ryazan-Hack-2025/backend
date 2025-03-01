import random
import uuid
from typing import Optional, List

from sqlalchemy import insert, select, delete, update

from config_data.config import Config, load_config
from src.transactions.models import Transaction
from src.database import async_session

settings: Config = load_config(".env")
global_vars = settings.variablesData


class TransactionRepository:
    async def generate_id(self) -> int:
        unique_id = random.randint(global_vars.MIN_ID, global_vars.MAX_ID)
        while await self.get_transaction_by_id(unique_id):
            unique_id = random.randint(global_vars.MIN_ID, global_vars.MAX_ID)

        return unique_id

    async def get_transaction_by_id(self, transaction_id: int) -> Transaction:
        async with async_session() as session:
            query = select(Transaction).where(Transaction.id == transaction_id)
            result = await session.execute(query)
            transaction = result.scalars().first()

        return transaction

    async def get_transaction_by_idempotency_key(self, idempotency_key: str):
        async with async_session() as session:
            query = select(Transaction).where(Transaction.idempotency_key == idempotency_key)
            result = await session.execute(query)
            transaction = result.scalars().first()

        return transaction

    async def get_all_buyer_transaction(self, buyer_id: int) -> List[Transaction]:
        async with async_session() as session:
            query = select(Transaction).where(Transaction.buyer_id == buyer_id)
            result = await session.execute(query)
            transactions = result.scalars().all()

        return transactions

    async def confirm_transaction(self, transaction_id: int) -> Transaction:
        async with async_session() as session:
            stmt = update(Transaction).where(Transaction.id == transaction_id).values(is_confirmed=True)
            await session.execute(stmt)
            await session.commit()

            transaction = await self.get_transaction_by_id(transaction_id)
            return transaction

    async def create_transaction(
            self, seller_inn: str, buyer_id: int, product_id: int, buy_count: int, price: int
    ) -> Transaction:
        transaction_id = await self.generate_id()
        idempotency_key = str(uuid.uuid4())

        async with async_session() as session:
            stmt = insert(Transaction).values(
                id=transaction_id,
                buy_count=buy_count,
                seller_inn=seller_inn,
                buyer_id=buyer_id,
                product_id=product_id,
                idempotency_key=idempotency_key,
                amount=buy_count * price
            )
            await session.execute(stmt)
            await session.commit()

        new_transaction = await self.get_transaction_by_id(transaction_id)
        return new_transaction
