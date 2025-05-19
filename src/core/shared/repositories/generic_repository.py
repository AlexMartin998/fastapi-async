from typing import Generic, List, Optional, Type, TypeVar
from src.core.database import AsyncSession
from sqlmodel import select, SQLModel

# from fastapi_pagination import Params, Page
# from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.sql import Select
from src.core.filter import FilterHook


ModelType = TypeVar("ModelType", bound=SQLModel)


class GenericRepository(Generic[ModelType]):
    """CRUD genérico para cualquier SQLModel."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    # async def find_all(
    #     self,
    #     params: Params,
    #     filters=None,
    # ) -> Page[ModelType]:
    #     query = select(self.model)
    #     if filters:
    #         query = filters.filter(query)
    #     return await paginate(self.session, query, params)

    async def find_all(
        self, filters=None
    ) -> List[ModelType]:
        if filters:
            query = filters.filter(
                select(self.model))
            result = await self.session.execute(query)
            return result.scalars().all()
        else:
            result = await self.session.execute(
                select(self.model)
            )
            return result.scalars().all()

    async def find_all_q(self, filters=None, extra_hooks: Optional[List[FilterHook]] = None) -> Select:
        q: Select = select(self.model)

        if filters:
            q = filters.filter(q)

        if extra_hooks:
            for hook in extra_hooks:
                q = hook(q)
        return q

    # async def find_all(
    #     self, offset: int = 0, limit: int = 10, filters=None
    # ) -> List[ModelType]:
    #     if filters:
    #         query = filters.filter(
    #             select(self.model).offset(offset).limit(limit))
    #         result = await self.session.execute(query)
    #         return result.scalars().all()
    #     else:
    #         result = await self.session.execute(
    #             select(self.model).offset(offset).limit(limit)
    #         )
    #         return result.scalars().all()

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
