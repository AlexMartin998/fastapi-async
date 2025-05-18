from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.core.config import settings


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
        if settings.ENV == "dev":
            await conn.run_sync(SQLModel.metadata.create_all)
        # En prod, usar Alembic


# 4. Dependency de FastAPI
async def get_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
