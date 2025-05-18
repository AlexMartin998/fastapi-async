from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError

from src.core.shared.exceptions.custom_exception import CustomException
from src.core.shared.exceptions.not_found_exception import NotFoundException


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: CustomException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):

    @app.exception_handler(CustomException)
    async def domain_exception(request: Request, exc: CustomException):
        if isinstance(exc, NotFoundException):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "message": exc.message,
                    "status": status.HTTP_404_NOT_FOUND,
                }
            )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
