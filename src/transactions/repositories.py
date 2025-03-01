import random
from typing import Optional, List

from sqlalchemy import insert, select, delete, update

from config_data.config import Config, load_config
from src.transactions.models import Transaction
from utils import auth_settings
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


