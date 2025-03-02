from datetime import datetime
from typing import Annotated, List
from pydantic import BaseModel, Field

from src.products.models import ProductCategory
from src.transactions.schemas import TransactionResponse


class ProductCreate(BaseModel):
    category: ProductCategory
    name: str
    price: int
    count: int
    description: str


class ProductEdit(BaseModel):
    category: ProductCategory
    name: str
    price: int
    count: int
    description: str


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    count: int
    description: str
    seller_inn: int
    category: ProductCategory
    created_at: datetime
    transactions: List[TransactionResponse]
