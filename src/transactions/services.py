import uuid
from typing import List

from yookassa import Payment, Configuration

from src.products.services import ProductService
from src.transactions.exceptions import NotFoundException, AccessException, ShortageProductException
from src.transactions.models import Transaction
from src.transactions.repositories import TransactionRepository
from src.users.models import User

from src.users.services import UserService

Configuration.account_id = "1043898"
Configuration.secret_key = "test_woZzHV9FDtczGpHyO1V0q-vwJh5-BRtCm-OOyNgLgcA"


class TransactionService:
    repository = TransactionRepository()

    async def get_transaction_by_id(self, transaction_id: str, user: User) -> Transaction:
        transaction = await self.repository.get_transaction_by_id(transaction_id)
        if transaction is None or transaction.buyer_id != user.id:
            raise NotFoundException()

        return transaction

    async def confirm_transaction(self, transaction_id: int, user: User) -> Transaction:
        transaction = await self.get_transaction_by_id(transaction_id, user)
        return await self.repository.confirm_transaction(transaction.id)

    async def get_all_buyer_transaction(self, user: User) -> List[Transaction]:
        return await self.repository.get_all_buyer_transaction(user.id)

    async def create_transaction(self, user: User, product_id: int, buy_count: int) -> str:
        product = await ProductService().get_product_by_id(product_id)
        if buy_count > product.count:
            raise ShortageProductException()

        amount = buy_count * product.price
        idempotency_key = str(uuid.uuid4())
        return_url = f"localhost/payment/{idempotency_key}"
        payment, idempotency_key = create_yookassa_payment(
            idempotency_key,
            amount, "Платёжка",
            return_url
        )

        payment_id = payment.id
        confirmation_url = payment.confirmation.confirmation_url

        await self.repository.create_transaction(
            payment_id, idempotency_key,
            product.seller_inn, user.id, product.id, buy_count,
            product.price
        )
        await ProductService().update_product_count(product_id, product.count - buy_count)

        print("HARA")
        return confirmation_url


def create_yookassa_payment(idempotency_key: str, amount: float, description: str,
                            return_url: str):
    payment = Payment.create(
        {
            "amount": {"value": amount, "currency": "RUB"},
            "confirmation": {"type": "redirect", "return_url": return_url},
            "capture": True,
            "description": description,
        },
        idempotency_key,
    )

    return payment, str(idempotency_key)
