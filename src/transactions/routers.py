from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, UploadFile, Query

from src.transactions.schemas import TransactionResponse
from src.transactions.services import TransactionService
from src.users.models import User
from src.users.services import UserService

router = APIRouter(tags=["transaction"], prefix="/transaction")


@router.get("/all", response_model=List[TransactionResponse])
async def get_all_buyer_transactions(
        current_user: Annotated[User, Depends(UserService().get_current_user)]
) -> List[TransactionResponse]:
    transactions = await TransactionService().get_all_buyer_transaction(current_user)
    return list(map(lambda x: TransactionResponse(**x.to_dict()), transactions))


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction_by_id(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        transaction_id: int
) -> TransactionResponse:
    transaction = await TransactionService().get_transaction_by_id(transaction_id, current_user)
    return TransactionResponse(**transaction.to_dict())


@router.post("/new", response_model=TransactionResponse)
async def create_new_transaction(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        product_id: int,
        buy_count: int
) -> TransactionResponse:
    transaction = await TransactionService().create_transaction(current_user, product_id, buy_count)
    return TransactionResponse(**transaction.to_dict())
