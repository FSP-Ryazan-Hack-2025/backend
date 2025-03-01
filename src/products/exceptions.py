from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Product not found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class AccessException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Access denied!"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
