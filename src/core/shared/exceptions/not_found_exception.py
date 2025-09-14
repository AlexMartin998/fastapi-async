from src.core.shared.exceptions.generic_exception import GenericException


class NotFoundException(GenericException):
    def __init__(self, message: str = "Resource not found", *, data: dict | None = None):
        super().__init__(message, status=404, data=data)
