from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from src.users.models import User, Seller
from src.users.schemas import UserCreate, Token, UserResponse, SuccessfulResponse, UserEdit, \
    SuccessfulGetVerifyCodeResponse, SuccessfulValidation, SellerCreate, SellerResponse
from src.users.services import UserService

buyer_router = APIRouter(tags=["user"], prefix="/user")
seller_router = APIRouter(tags=["seller"], prefix="/seller")


@buyer_router.post("/register")
async def register(user_create: UserCreate) -> Token:
    user = await UserService().create_user(user_create)
    access_token = UserService().create_access_token(user)
    refresh_token = UserService().create_refresh_token(user)
    return Token(access_token=access_token, refresh_token=refresh_token)


@seller_router.post("/register")
async def register(seller_create: SellerCreate) -> Token:
    seller = await UserService().create_seller(seller_create)
    access_token = UserService().create_seller_access_token(seller)
    refresh_token = UserService().create_seller_refresh_token(seller)
    return Token(access_token=access_token, refresh_token=refresh_token)


@buyer_router.post("/login", response_model=Token)
async def authenticate_user_jwt(user: User = Depends(UserService().authenticate_user)) -> Token:
    access_token = UserService().create_access_token(user)
    refresh_token = UserService().create_refresh_token(user)
    return Token(access_token=access_token, refresh_token=refresh_token)


@seller_router.post("/login", response_model=Token)
async def authenticate_seller_jwt(seller: Seller = Depends(UserService().authenticate_seller)) -> Token:
    access_token = UserService().create_seller_access_token(seller)
    refresh_token = UserService().create_seller_refresh_token(seller)
    return Token(access_token=access_token, refresh_token=refresh_token)


@buyer_router.post("/refresh", response_model=Token, response_model_exclude_none=True)
async def refresh_jwt(
        user: Annotated[User, Depends(UserService().get_current_user_for_refresh)]
) -> Token:
    access_token = UserService().create_access_token(user)
    return Token(access_token=access_token)


@seller_router.post("/refresh", response_model=Token, response_model_exclude_none=True)
async def refresh_jwt(
        seller: Annotated[Seller, Depends(UserService().get_current_seller_for_refresh)]
) -> Token:
    access_token = UserService().create_seller_access_token(seller)
    return Token(access_token=access_token)


@buyer_router.get("/register/verify_code", response_model=SuccessfulGetVerifyCodeResponse)
async def get_verify_code_by_email(email: str) -> SuccessfulGetVerifyCodeResponse:
    await UserService().get_verify_code(email)
    return SuccessfulGetVerifyCodeResponse()


@buyer_router.post("/register/verify_code", response_model=SuccessfulValidation)
async def check_code_from_email(email: str, code: int) -> SuccessfulValidation:
    if await UserService().check_verify_code(email, code):
        return SuccessfulValidation()


@buyer_router.post("/edit_password", response_model=SuccessfulResponse)
async def edit_user_password(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        new_password: str
) -> SuccessfulResponse:
    await UserService().edit_user_password(current_user, new_password)
    return SuccessfulResponse()


@buyer_router.get("/self", response_model=UserResponse)
async def login_buyer_for_access_token(
        current_user: Annotated[User, Depends(UserService().get_current_user)]
) -> UserResponse:
    return UserResponse(**current_user.to_dict())


@buyer_router.get("/{buyer_id}", response_model=UserResponse)
async def get_buyer_by_id(buyer_id: int) -> UserResponse:
    buyer = await UserService().get_user_by_id(buyer_id)
    return UserResponse(**buyer.to_dict())


@seller_router.get("/self", response_model=SellerResponse)
async def login_seller_for_access_token(
        current_seller: Annotated[Seller, Depends(UserService().get_current_seller)]
) -> SellerResponse:
    return SellerResponse(**current_seller.to_dict())


@seller_router.get("/{seller_inn}", response_model=SellerResponse)
async def get_seller_by_id(seller_inn: str) -> SellerResponse:
    seller = await UserService().get_seller_by_inn(seller_inn)
    return SellerResponse(**seller.to_dict())


@buyer_router.put("/edit", response_model=UserResponse)
async def edit_user(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        user_edit: UserEdit
) -> UserResponse:
    upd_user = await UserService().edit_user_info(current_user, user_edit)
    return UserResponse(**upd_user.to_dict())


@buyer_router.delete("/", response_model=SuccessfulResponse)
async def delete_user(
        current_user: Annotated[User, Depends(UserService().get_current_user)]
) -> SuccessfulResponse:
    await UserService().delete_user(current_user)
    return SuccessfulResponse()


@seller_router.delete("/", response_model=SuccessfulResponse)
async def delete_seller(
        current_seller: Annotated[Seller, Depends(UserService().get_current_seller)]
) -> SuccessfulResponse:
    await UserService().delete_seller(current_seller)
    return SuccessfulResponse()
