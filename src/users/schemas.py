from datetime import datetime, date
from typing import Annotated, List
from pydantic import BaseModel, Field

from src.products.schemas import ProductResponse
from src.users.models import Role


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class SuccessfulGetVerifyCodeResponse(BaseModel):
    success: str = "The verify code has been successfully sent to the email"


class SuccessfulValidation(BaseModel):
    success: str = "Successful Validation!"


class TokenData(BaseModel):
    email: str | None = None


class SellerTokenData(BaseModel):
    inn: str | None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class SellerCreate(BaseModel):
    inn: str
    name: str
    surname: str
    patronymic: str
    passport_series: int
    passport_number: int
    birthday_date: date
    role: Role
    password: Annotated[str, Field(min_length=2, max_length=25)]


class SellerLogin(BaseModel):
    inn: str
    password: Annotated[str, Field(min_length=2, max_length=25)]


class SellerResponse(BaseModel):
    inn: str
    name: str
    surname: str
    patronymic: str
    about: str
    role: Role
    created_at: datetime
    products: List[ProductResponse]


class UserCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    surname: Annotated[str, Field(min_length=2, max_length=50)]
    patronymic: Annotated[str, Field(min_length=2, max_length=50)]
    email: Annotated[str, Field(min_length=2, max_length=50)]
    password: Annotated[str, Field(min_length=2, max_length=25)]


class UserLogin(BaseModel):
    email: Annotated[str, Field(min_length=2, max_length=50)]
    password: Annotated[str, Field(min_length=2, max_length=25)]


class UserEdit(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    surname: Annotated[str, Field(min_length=2, max_length=50)]
    patronymic: Annotated[str, Field(min_length=2, max_length=50)]


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    email: str
    created_at: datetime
