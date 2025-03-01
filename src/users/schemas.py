from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field

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
    inn: int | None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class SellerCreate(BaseModel):
    inn: int
    password: Annotated[str, Field(min_length=2, max_length=25)]


class SellerLogin(BaseModel):
    inn: int
    password: Annotated[str, Field(min_length=2, max_length=25)]


class SellerResponse(BaseModel):
    inn: int
    name: str
    surname: str
    patronymic: str
    about: str
    role: Role
    created_at: datetime


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
