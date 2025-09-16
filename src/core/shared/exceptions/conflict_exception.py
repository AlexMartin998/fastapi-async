from src.core.shared.exceptions.generic_exception import GenericException


class ConflictException(GenericException):
    def __init__(self, message: str = "Conflict", *, data: dict | None = None):
        super().__init__(message, status=409, data=data)
