from typing import Generic, TypeVar, List, Optional
from sqlmodel import SQLModel

from sqlalchemy.sql import Select
from src.core.filter import FilterHook
# from fastapi_pagination.ext.sqlalchemy import paginate


from src.core.shared.exceptions.not_found_exception import NotFoundException

ModelType = TypeVar("ModelType", bound=SQLModel)


class GenericService(Generic[ModelType]):
    """Lógica de negocio genérica con validaciones comunes."""

    def __init__(self, repository):
        self.repo = repository  # instancia de GenericRepository

    # async def find_all(
    #     self,
    #     params: Params,
    #     filters=None,
    # ) -> Page[ModelType]:
    #     return await self.repo.find_all(params, filters)

    # async def find_all(self, offset: int, limit: int, filters=None) -> List[ModelType]:
    #     return await self.repo.find_all(offset, limit, filters)

    async def find_all(self, filters=None, params=None) -> List[ModelType]:
        # return await self.repo.find_all(filters)
        extra_hooks: Optional[List[FilterHook]] = None
        q: Select = await self.repo.find_all_q(filters, extra_hooks)
        result = await self.repo.session.execute(q)
        # return await paginate(self.repo.session, q, params)
        return result.scalars().all()

    async def find_all_q(
        self,
        filters=None,
        # extra_hooks: Optional[List[FilterHook]] = None,
    ) -> Select:
        extra_hooks: Optional[List[FilterHook]] = None
        return await self.repo.find_all_q(filters, extra_hooks)

    async def find_one(self, obj_id: int) -> ModelType:
        obj = await self.repo.find_one(obj_id)
        if not obj:
            raise NotFoundException(
                message=f"Object with id {obj_id} not found")
        return obj

    async def create(self, create_dto) -> ModelType:
        instance = self.repo.model(**create_dto.dict())
        created = await self.repo.create(instance)
        await self.repo.commit()
        return created

    async def update(self, obj_id: int, update_dto) -> ModelType:
        obj = await self.find_one(obj_id)
        for field, value in update_dto.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        updated = await self.repo.update(obj)
        await self.repo.commit()
        return updated

    async def delete(self, obj_id: int) -> None:
        obj = await self.find_one(obj_id)
        await self.repo.delete(obj)
        await self.repo.commit()
