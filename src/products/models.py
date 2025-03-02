import datetime

from enum import Enum
from typing import Dict, Any, List

from sqlalchemy import func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ProductCategory(Enum):
    clothing = "Одежда"
    shoes = "Обувь"
    accessories = "Аксессуары"
    electronics = "Электроника"
    home_goods = "Товары для дома"
    books = "Книги"
    sports_and_outdoors = "Спорт и отдых"
    beauty_and_personal_care = "Красота и личная гигиена"
    toys_and_games = "Игрушки и игры"
    food_and_beverages = "Продукты питания и напитки"
    other = "Другое"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[ProductCategory] = mapped_column(default=ProductCategory.other)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    count: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    seller_inn: Mapped[int] = mapped_column(ForeignKey("sellers.inn", ondelete="CASCADE"))
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

    seller: Mapped["Seller"] = relationship(back_populates="products", uselist=False)

    transactions: Mapped[List["Transaction"]] = relationship(back_populates="product", uselist=True, lazy="selectin",
                                                             cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "count": self.count,
            "description": self.description,
            "seller_inn": self.seller_inn,
            "created_at": self.created_at,
            "transactions": [transaction.to_dict() for transaction in self.transactions]
        }
