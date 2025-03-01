from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, UploadFile, Query, Request

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


@router.post("/notifications")
async def payment_confirm(request: Request):
    req_json = await request.json()
    print(req_json)

    if req_json["event"] == "payment.succeeded":
        payment_id = req_json["object"]["id"]
        print(payment_id)

        return "success"

    return "bruh"


@router.get("/{transaction_id}")
async def get_transaction_by_id(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        transaction_id: str
) -> TransactionResponse:
    transaction = await TransactionService().get_transaction_by_id(transaction_id, current_user)
    return TransactionResponse(**transaction.to_dict())


@router.post("/new")
async def create_new_transaction(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        product_id: int,
        buy_count: int
) -> str:
    return await TransactionService().create_transaction(current_user, product_id, buy_count)
