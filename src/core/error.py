from typing import Any, Callable
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError


from src.core.shared.exceptions.custom_exception import CustomException
from src.core.shared.exceptions.generic_exception import GenericException
from src.core.shared.exceptions.conflict_exception import ConflictException
from src.core.shared.exceptions.not_found_exception import NotFoundException


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    """
    Factoría simple por si quieres registrar handlers ad-hoc
    para ciertos casos (no es lo común).
    """
    async def exception_handler(_: Request, __: CustomException):
        return JSONResponse(content=initial_detail, status_code=status_code)
    return exception_handler


def register_all_errors(app: FastAPI) -> None:
    """
    Registra todos los handlers de errores:
    - GenericException: aware de HTTP (status + data)
    - CustomException: dominio puro -> 500 (o lo que definas)
    - StarletteHTTPException: HTTPException lanzada por FastAPI/Starlette
    - SQLAlchemyError: fallback de errores de ORM
    - 500: último recurso
    """

    # 1) HTTPException nativa de FastAPI/Starlette
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    # 2) Excepciones “transport-aware”: tienen status y data
    @app.exception_handler(GenericException)
    async def generic_exception_handler(_: Request, exc: GenericException):
        # Estructura estable de error
        body = {"message": exc.message, "status": exc.status}
        if getattr(exc, "data", None):
            # Mezcla data (columns/values/constraint/etc.)
            body |= exc.data
        return JSONResponse(status_code=exc.status, content=body)

    # 3) Excepciones de dominio puras (no aware). Pueden provenir de services.
    @app.exception_handler(CustomException)
    async def custom_exception_handler(_: Request, exc: CustomException):
        # Si en tu proyecto NotFound/Conflict heredan de CustomException (y no de Generic),
        # cúbrelas aquí de forma específica:
        if isinstance(exc, NotFoundException):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": exc.message, "status": 404},
            )
        if isinstance(exc, ConflictException):
            # Nota: si ConflictException hereda de GenericException, no entrará aquí
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"message": exc.message, "status": 409},
            )

        # Fallback: dominio puro -> 500 genérico (no acoplamos a HTTP)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": exc.message or "Internal Server Error"},
        )

    # 4) Errores SQLAlchemy no capturados por la capa de dependencia
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(_: Request, __: SQLAlchemyError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Database error"},
        )

    # 5) Fallback 500 explícito
    @app.exception_handler(500)
    async def internal_server_error(_: Request, __: Exception):
        return JSONResponse(
            content={"message": "Oops! Something went wrong",
                     "error_code": "server_error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
