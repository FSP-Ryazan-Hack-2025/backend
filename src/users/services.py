import os
import shutil
import smtplib
from pathlib import Path

import jwt

from datetime import timedelta
from typing import Optional, List
from fastapi import Depends, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config_data.config import Config, load_config
from utils.auth_settings import validate_password, decode_jwt, encode_jwt

from src.users.models import User, Seller
from src.users.repositories import UserRepository
from src.users.schemas import UserCreate, TokenData, UserEdit, UserLogin, SuccessfulResponse, SellerLogin, \
    SellerTokenData, SellerCreate
from src.users.exceptions import CredentialException, TokenTypeException, NotFoundException, AccessException, \
    EmailExistsException, ErrorLoadAvatarException, ErrorDeleteAvatarException, EmailSenderException, \
    IncorrectEmailAddressException, IncorrectVerifyCodeException, SellerExistsException
from utils.email_sender import send_verification_code

http_bearer = HTTPBearer()

settings: Config = load_config(".env")
auth_config = settings.authJWT

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


class UserService:
    repository = UserRepository()

    @staticmethod
    def create_jwt(
            token_type: str,
            token_data: dict,
            expire_minutes: int = auth_config.access_token_expire_minutes,
            expire_timedelta: timedelta | None = None
    ) -> str:
        jwt_payload = {TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        token = encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta
        )
        return token

    async def get_verify_code(self, email: str) -> None:
        potential_user = await self.repository.get_user_by_email(email)
        if potential_user is not None:
            raise EmailExistsException()

        try:
            code = send_verification_code(email)
            potential_code = await self.repository.get_verify_code_by_email(email)
            if potential_code is not None:
                await self.repository.update_verify_code(email, code)
            else:
                await self.repository.create_verify_code(email, code)

        except smtplib.SMTPRecipientsRefused as e:
            raise IncorrectEmailAddressException()
        except Exception as e:
            raise EmailSenderException()

    async def check_verify_code(self, email: str, code: int) -> bool:
        verify_code = await self.repository.get_verify_code_by_email(email)
        if verify_code is None:
            raise IncorrectEmailAddressException()

        if verify_code.code != code:
            raise IncorrectVerifyCodeException()

        await self.repository.delete_verify_code_by_id(verify_code.id)
        return True

    def create_access_token(self, user: User) -> str:
        jwt_payload = {
            "sub": user.email,
        }
        return self.create_jwt(
            token_type=ACCESS_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_minutes=auth_config.access_token_expire_minutes
        )

    def create_seller_access_token(self, seller: Seller) -> str:
        jwt_payload = {
            "sub": seller.inn,
        }
        return self.create_jwt(
            token_type=ACCESS_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_minutes=auth_config.access_token_expire_minutes
        )

    def create_refresh_token(self, user: User) -> str:
        jwt_payload = {
            "sub": user.email
        }
        return self.create_jwt(
            token_type=REFRESH_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_timedelta=timedelta(days=auth_config.refresh_token_expire_days)
        )

    def create_seller_refresh_token(self, seller: Seller) -> str:
        jwt_payload = {
            "sub": seller.inn
        }
        return self.create_jwt(
            token_type=REFRESH_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_timedelta=timedelta(days=auth_config.refresh_token_expire_days)
        )

    async def authenticate_user(self, user_login: UserLogin) -> Optional[User]:
        user = await self.repository.get_user_by_email(user_login.email)
        if not user:
            raise CredentialException()
        if not validate_password(user_login.password, user.password_hash):
            raise CredentialException()

        return user

    async def authenticate_seller(self, seller_login: SellerLogin) -> Optional[Seller]:
        seller = await self.repository.get_seller_by_inn(seller_login.inn)
        if not seller:
            raise CredentialException()
        if not validate_password(seller_login.password, seller.password_hash):
            raise CredentialException()

        return seller

    @staticmethod
    async def validate_admin_user(user) -> User:
        if not user.is_admin:
            raise AccessException()
        return user

    async def validate_user(self, expected_token_type: str, token: str | bytes) -> User:

        try:
            payload = decode_jwt(token=token)
            token_type = payload.get(TOKEN_TYPE_FIELD)
            if token_type != expected_token_type:
                raise TokenTypeException(token_type, expected_token_type)

            email: str = payload.get("sub")
            if email is None or not isinstance(email, str):
                raise CredentialException()
            token_data = TokenData(email=email)

        except jwt.DecodeError:
            raise CredentialException()
        except jwt.ExpiredSignatureError:
            raise CredentialException()

        user = await self.repository.get_user_by_email(token_data.email)
        if user is None:
            raise CredentialException()

        return user

    async def validate_seller(self, expected_token_type: str, token: str | bytes) -> Seller:
        try:
            payload = decode_jwt(token=token)
            token_type = payload.get(TOKEN_TYPE_FIELD)
            if token_type != expected_token_type:
                raise TokenTypeException(token_type, expected_token_type)

            inn: int = payload.get("sub")
            if inn is None or not isinstance(inn, int):
                raise CredentialException()
            token_data = SellerTokenData(inn=inn)

        except jwt.DecodeError:
            raise CredentialException()
        except jwt.ExpiredSignatureError:
            raise CredentialException()

        seller = await self.repository.get_seller_by_inn(token_data.inn)
        if seller is None:
            raise CredentialException()

        return seller

    async def add_avatar(self, avatar: UploadFile, user: User) -> SuccessfulResponse:
        root = Path(__file__).parent.parent.parent
        avatar_path = os.path.join(root, "assets", "avatars", f"{user.id}.webp")

        try:
            with open(avatar_path, "wb+") as avatar_obj:
                shutil.copyfileobj(avatar.file, avatar_obj)
        except Exception as e:
            print("Error loading avatar:", e)
            raise ErrorLoadAvatarException()

        return SuccessfulResponse()

    async def get_avatar_url(self, user: User) -> str:
        return f"static/avatars/{user.id}.webp"

    async def delete_avatar(self, user: User) -> SuccessfulResponse:
        root = Path(__file__).parent.parent.parent
        avatar_path = os.path.join(root, "assets", "avatars", f"{user.id}.webp")

        try:
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
        except Exception as e:
            print("Error deleting avatar:", e)
            raise ErrorDeleteAvatarException()

        return SuccessfulResponse()

    async def get_current_user_for_refresh(self, token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> User:
        return await self.validate_user(expected_token_type=REFRESH_TOKEN_TYPE, token=token.credentials)

    async def get_current_seller_for_refresh(
            self,
            token: HTTPAuthorizationCredentials = Depends(http_bearer)
    ) -> Seller:
        return await self.validate_seller(expected_token_type=REFRESH_TOKEN_TYPE, token=token.credentials)

    async def get_current_user(self, token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> User:
        return await self.validate_user(expected_token_type=ACCESS_TOKEN_TYPE, token=token.credentials)

    async def get_current_seller(
            self,
            token: HTTPAuthorizationCredentials = Depends(http_bearer)
    ) -> Seller:
        return await self.validate_seller(expected_token_type=ACCESS_TOKEN_TYPE, token=token.credentials)

    async def get_current_admin_user(self, token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> User:
        current_user = await self.get_current_user(token)
        return await self.validate_admin_user(current_user)

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.repository.get_user_by_id(user_id)
        if user is None:
            raise NotFoundException()
        return user

    async def get_all_users(self) -> List[User]:
        return await self.repository.get_all_users()

    async def create_user(self, user: UserCreate) -> User:
        if await self.repository.get_user_by_email(user.email) is not None:
            raise EmailExistsException()

        return await self.repository.create_user(user)

    async def create_seller(self, seller: SellerCreate):
        if await self.repository.get_seller_by_inn(seller.inn) is not None:
            raise SellerExistsException()

        return await self.repository.create_seller(seller)

    async def edit_user_info(self, user: User, user_edit: UserEdit) -> User:
        return await self.repository.edit_info(user, user_edit)

    async def edit_user_password(self, user: User, password: str) -> None:
        return await self.repository.edit_password(user, password)

    async def change_admin_status(self, user_id: int) -> User:
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise NotFoundException()
        if user.is_admin:
            raise AccessException()

        return await self.repository.change_admin_status(user)

    async def change_verified_status(self, user_id: int) -> User:
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise NotFoundException()
        if user.is_admin:
            raise AccessException()

        return await self.repository.change_verified_status(user)

    async def change_active_status(self, user_id: int) -> User:
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise NotFoundException()
        if user.is_admin:
            raise AccessException()

        return await self.repository.change_active_status(user)

    async def delete_user(self, user: User) -> None:
        return await self.repository.delete_user(user)

    async def delete_user_by_id(self, user_id: int):
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise NotFoundException()
        if user.is_admin:
            raise AccessException()

        return await self.repository.delete_user(user)

    async def remove_user_admin_status(self, user_id: int) -> None:
        return await self.repository.remove_user_admin_status(user_id)

    async def remove_admin_status_for_all(self) -> None:
        return await self.repository.remove_admin_status_for_all()

    async def delete_all_users(self) -> None:
        return await self.repository.delete_all_users()
