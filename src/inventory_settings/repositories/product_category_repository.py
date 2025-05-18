from sqlmodel.ext.asyncio.session import AsyncSession

from src.inventory_settings.models.product_category_model import ProductCategory
from src.core.shared.repositories.generic_repository import GenericRepository


class CategoryRepository(GenericRepository[ProductCategory]):

    def __init__(self, session: AsyncSession):
        super().__init__(ProductCategory, session)
