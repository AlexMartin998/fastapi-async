# src/core/shared/repositories/generic_repository.py

from typing import Generic, List, Optional, Type, TypeVar
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)


class GenericRepository(Generic[ModelType]):
    """CRUD genérico para cualquier SQLModel."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def find_all(
        self, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = await self.session.execute(
            select(self.model).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def find_one(self, obj_id: int) -> Optional[ModelType]:
        return await self.session.get(self.model, obj_id)

    async def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(self, obj: ModelType) -> ModelType:
        await self.session.flush()
        return obj

    async def delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)

    async def commit(self) -> None:
        await self.session.commit()
