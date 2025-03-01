import datetime

from enum import Enum
from typing import Dict, Any

from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Role(str, Enum):
    buyer = "buyer"
    self_employed = "selfEmployed"
    individual_entrepreneur = "individual"
    organization = "company"


class Seller(Base):
    __tablename__ = "sellers"

    inn: Mapped[str] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(50), default="")
    surname: Mapped[str] = mapped_column(String(50), default="")
    patronymic: Mapped[str] = mapped_column(String(50), default="")
    about: Mapped[str] = mapped_column(String(1000), nullable=True, default="")
    role: Mapped[Role] = mapped_column(default=Role.self_employed)

    password_hash: Mapped[bytes] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now(), nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "inn": self.inn,
            "name": self.name,
            "surname": self.surname,
            "patronymic": self.patronymic,
            "about": self.about,
            "role": self.role.value,
            "created_at": self.created_at
        }


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(50), nullable=False, default="testPatronymic")
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    role: Mapped[Role] = mapped_column(default=Role.buyer, nullable=True)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now(), nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "patronymic": self.patronymic,
            "email": self.email,
            "created_at": self.created_at
        }


class VerifyCode(Base):
    __tablename__ = "verify_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    code: Mapped[int] = mapped_column(nullable=False)
