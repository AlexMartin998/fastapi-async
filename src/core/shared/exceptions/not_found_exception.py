from .custom_exception import CustomException


class NotFoundException(CustomException):
    def __init__(self, message="Resource not found"):
        super().__init__(message)
