from app.exceptions.base_exception import BaseAppException

class ApiException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, type="ApiException", retryable=False)
