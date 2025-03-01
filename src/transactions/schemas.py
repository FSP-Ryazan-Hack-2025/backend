from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field


class TransactionResponse(BaseModel):
    id: int
    seller_inn: str
    buyer_id: int
    buy_count: int
    product_id: int
    created_at: datetime
