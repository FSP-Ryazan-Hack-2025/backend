from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Transaction not found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ShortageProductException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "There are fewer items in stock than you specified."

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class AccessException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Access denied!"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
