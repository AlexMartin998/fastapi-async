from src.core.shared.exceptions.custom_exception import CustomException


class GenericException(CustomException):

    def __init__(self, message: str = "Error", *, status: int = 400, data: dict | None = None):
        super().__init__(message)
        self.status = status
        self.data = data or {}
