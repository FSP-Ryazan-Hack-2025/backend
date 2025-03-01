import datetime

from enum import Enum
from typing import Dict, Any

from sqlalchemy import func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    buy_count: Mapped[int] = mapped_column()
    seller_inn: Mapped[str] = mapped_column(ForeignKey("sellers.inn", ondelete="CASCADE"))
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    amount: Mapped[int] = mapped_column(nullable=True)
    is_confirmed: Mapped[bool] = mapped_column(default=False, nullable=True)
    idempotency_key: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "seller_inn": self.seller_inn,
            "buyer_id": self.buyer_id,
            "buy_count": self.buy_count,
            "amount": self.amount,
            "product_id": self.product_id,
            "created_at": self.created_at
        }
