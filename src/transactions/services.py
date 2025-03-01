import uuid
from typing import List

from src.products.services import ProductService
from src.transactions.exceptions import NotFoundException, AccessException, ShortageProductException
from src.transactions.models import Transaction
from src.transactions.repositories import TransactionRepository
from src.users.models import User
from yookassa import Payment

from src.users.services import UserService


class TransactionService:
    repository = TransactionRepository()

    async def get_transaction_by_id(self, transaction_id: int, user: User) -> Transaction:
        transaction = await self.repository.get_transaction_by_id(transaction_id)
        if transaction is None or transaction.buyer_id != user.id:
            raise NotFoundException()

        return transaction

    async def confirm_transaction(self, transaction_id: int, user: User) -> Transaction:
        transaction = await self.get_transaction_by_id(transaction_id, user)
        return await self.repository.confirm_transaction(transaction.id)

    async def get_all_buyer_transaction(self, user: User) -> List[Transaction]:
        return await self.repository.get_all_buyer_transaction(user.id)

    async def create_transaction(self, user: User, product_id: int, buy_count: int) -> Transaction:
        product = await ProductService().get_product_by_id(product_id)
        if buy_count > product.count:
            raise ShortageProductException()

        transaction = await self.repository.create_transaction(
            product.seller_inn, user.id, product.id, buy_count, product.price
        )
        await ProductService().update_product_count(product_id, product.count - buy_count)

        return transaction
