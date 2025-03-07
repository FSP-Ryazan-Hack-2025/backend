from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field


class TransactionResponse(BaseModel):
    id: str
    seller_inn: str
    buyer_id: int
    buy_count: int
    product_id: int
    amount: int
    created_at: datetime
