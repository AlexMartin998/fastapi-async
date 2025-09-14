from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.core.settings import settings
from src.core.shared.exceptions.conflict_exception import ConflictException
from src.core.shared.exceptions.generic_exception import GenericException
from src.core.helpers.db_error_helper import format_db_error


# 1. Engine asíncrono con asyncpg
async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=300,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)


# 2. Factory de sesiones
AsyncSessionFactory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# 3. Inicialización de esquema (solo DEV)
async def init_db():
    async with async_engine.begin() as conn:
        pass
        # ## dev to automatically create tables ---
        # if settings.ENV == "dev":
        #     await conn.run_sync(SQLModel.metadata.create_all)
        # En prod, usar Alembic


# 4. Dependency de FastAPI
async def get_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            data = format_db_error(e)
            err = data.get("error")

            if err == "unique_violation":
                # 409 por duplicado
                raise ConflictException(data["message"], data=data) from e

            if err in ("not_null_violation", "string_too_long", "check_violation"):
                # 422 datos inválidos
                raise GenericException(
                    data["message"], status=422, data=data) from e

            if err == "foreign_key_violation":
                # 409 o 400 según tu contrato (aquí 409)
                raise GenericException(
                    data["message"], status=409, data=data) from e

            # Fallback
            raise GenericException(
                "Error de integridad.", status=409, data=data) from e
        except SQLAlchemyError as e:
            await session.rollback()
            raise GenericException(
                "Error de base de datos.", status=500) from e
