from src.core.shared.services.generic_service import GenericService

from src.inventory_settings.models.product_category_model import ProductCategory
from src.inventory_settings.repositories.product_category_repository import CategoryRepository


class CategoryService(GenericService[ProductCategory]):

    def __init__(self, repo: CategoryRepository):
        super().__init__(repo)
