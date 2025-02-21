from typing import Annotated
from pydantic import BaseModel, Field

from src.users.models import Gender


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class TokenData(BaseModel):
    email: str | None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    surname: Annotated[str, Field(min_length=2, max_length=50)]
    email: Annotated[str, Field(min_length=2, max_length=50)]
    gender: Gender
    password: Annotated[str, Field(min_length=2, max_length=25)]


class UserLogin(BaseModel):
    email: Annotated[str, Field(min_length=2, max_length=50)]
    password: Annotated[str, Field(min_length=2, max_length=25)]


class UserEdit(BaseModel):
    name: str
    surname: str
    gender: Gender


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    gender: Gender
