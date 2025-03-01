from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    buy_count: int
