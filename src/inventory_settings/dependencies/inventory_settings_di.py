from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.database import get_session
from src.inventory_settings.repositories.product_category_repository import (
    CategoryRepository,
)
from src.inventory_settings.services.product_category_service import (
    CategoryService,
)


async def get_category_repo(
    session: AsyncSession = Depends(get_session)
) -> CategoryRepository:
    return CategoryRepository(session)


async def get_category_service(
    repo: CategoryRepository = Depends(get_category_repo)
) -> CategoryService:
    return CategoryService(repo)
