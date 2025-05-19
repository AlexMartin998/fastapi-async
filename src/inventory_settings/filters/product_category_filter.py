from typing import Optional
from src.core.filter import make_filter_for_model
from src.inventory_settings.models.product_category_model import ProductCategory

BaseCategoryFilter = make_filter_for_model(ProductCategory)


class ProductCategoryFilter(BaseCategoryFilter):
    custom_qsb: Optional[bool] = None

    class Constants(BaseCategoryFilter.Constants):
        model = ProductCategory

    def filter(self, query):
        # 1) Si viene flag, aplicamos lógica custom
        if self.custom_qsb:
            query = query.where(
                ProductCategory.is_active.is_(True),
                ProductCategory.code.ilike("%2%")
            )

        # clean custom fields that are not in the model ---
        # setattr(self, "custom_qsb", None)
        delattr(self, "custom_qsb")

        return super().filter(query)


# from typing import Optional
# from fastapi_filter.contrib.sqlalchemy import Filter

# from src.inventory_settings.models.product_category_model import ProductCategory


# class ProductCategoryFilter(Filter):
#     code: Optional[str] = None
#     name: Optional[str] = None

#     code__like:    Optional[str] = None    # case-sensitive LIKE '%value%'
#     code__ilike:   Optional[str] = None    # case-insensitive LIKE '%value%'
#     name__like:    Optional[str] = None
#     name__ilike:   Optional[str] = None
#     description__ilike: Optional[str] = None

#     class Constants(Filter.Constants):
#         model = ProductCategory
