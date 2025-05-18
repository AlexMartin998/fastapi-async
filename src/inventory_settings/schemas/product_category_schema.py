from uuid import UUID
from datetime import datetime

from src.inventory_settings.models.product_category_model import ProductCategoryBase


class ProductCategoryRead(ProductCategoryBase):
    id: int
    uuid: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(ProductCategoryBase):
    pass
