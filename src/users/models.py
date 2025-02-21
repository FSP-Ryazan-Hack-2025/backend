import datetime

from enum import Enum
from typing import Dict, Any

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Gender(Enum):
    male = "male"
    female = "female"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    gender: Mapped[Gender] = mapped_column(default=Gender.male)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    password_hash: Mapped[bytes] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "gender": self.gender.value,
            "is_admin": self.is_admin,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "created_at": self.created_at,
        }
