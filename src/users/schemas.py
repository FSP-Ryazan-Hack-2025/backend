from datetime import datetime
from pydantic import BaseModel

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
    name: str
    surname: str
    email: str
    gender: Gender
    password: str


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
    is_admin: bool
    is_verified: bool
    is_active: bool
    created_at: datetime
