from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field

from src.products.models import ProductCategory


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
    created_at: datetime
