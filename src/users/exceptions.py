from fastapi import HTTPException, status


class EmailExistsException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User with this email already exists"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class SellerExistsException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "This inn already registered"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidInnFirstException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "This INN does not belong to company or individual entrepreneur"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidInnSecondException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "This INN does not belong to self employed"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class InnIncorrectStatusException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Incorrect INN-person role"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ErrorLoadAvatarException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Can't load avatar"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ErrorDeleteAvatarException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Can't delete avatar"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CredentialException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


class TokenTypeException(HTTPException):

    def __new__(cls, *args, **kwargs):
        cls.detail = f"Invalid token type {args[0]!r} expected {args[1]!r}"
        cls.status_code = status.HTTP_401_UNAUTHORIZED

        return super().__new__(cls)

    def __init__(self, *args):  # noqa
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class AccessException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Access denied!"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class EmailSenderException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to send code to email"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectEmailAddressException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid email address"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectVerifyCodeException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect verification code"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
