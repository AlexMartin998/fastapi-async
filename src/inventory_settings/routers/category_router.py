from fastapi import APIRouter, status, Depends, Query
from typing import List


from src.inventory_settings.dependencies.inventory_settings_di import (
    get_category_service,
)
from src.inventory_settings.schemas.product_category_schema import (
    ProductCategoryRead,
    ProductCategoryCreate,
    ProductCategoryUpdate,
)
from src.inventory_settings.services.product_category_service import CategoryService


router = APIRouter(prefix="/categories", tags=["categories"])



# from fastapi_filter import FilterDepends
# from sqlmodel import select
# from src.core.database import get_session, AsyncSession
# from src.inventory_settings.models.product_category_model import ProductCategory
# from src.inventory_settings.filters.product_category_filter import (
#     ProductCategoryFilter
# )

# @router.get("/", response_model=List[ProductCategoryRead])
# async def list_categories(
#     category_filter: ProductCategoryFilter = FilterDepends(ProductCategoryFilter),
#     # category_filter: FilterDepends = FilterDepends(make_filter_for_model(ProductCategory)),
#     session:        AsyncSession    = Depends(get_session),
# ):
#     query  = category_filter.filter(select(ProductCategory))
#     result = await session.execute(query)       # execute() existe aquí
#     return result.scalars().all()               # scalars() extrae tus modelos




# from fastapi_filter import FilterDepends
# from src.inventory_settings.filters.product_category_filter import (
#     ProductCategoryFilter
# )

# @router.get("/", response_model=List[ProductCategoryRead])
# async def list_categories(
#     filters: ProductCategoryFilter = FilterDepends(ProductCategoryFilter),
#     service: CategoryService = Depends(get_category_service),
#     limit: int = Query(100, le=200),
#     offset: int = Query(0, ge=0),
# ):
#     return await service.find_all(
#         offset=offset,
#         limit=limit,
#         filters=filters,
#     )

from fastapi_filter import FilterDepends
from src.inventory_settings.filters.product_category_filter import (
    ProductCategoryFilter
)
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate

@router.get("/", response_model=Page[ProductCategoryRead])
async def list_categories(
    filters: ProductCategoryFilter = FilterDepends(ProductCategoryFilter),
    service: CategoryService = Depends(get_category_service),
    params: Params = Depends(),
):
    # paginate internamente construye la respuesta con meta y items
    # return await service.find_all(filters=filters)
    # q = filters.filter(
    #     select(service.repo.model)
    # )
    q = await service.find_all_q(filters=filters)
    return await paginate(service.repo.session, q, params)



@router.get("/{category_id}", response_model=ProductCategoryRead)
async def get_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
):
    return await service.find_one(category_id)


@router.post("/", response_model=ProductCategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    dto: ProductCategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    return await service.create(dto)


@router.patch("/{category_id}", response_model=ProductCategoryRead)
async def update_category(
    category_id: int,
    dto: ProductCategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    return await service.update(category_id, dto)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
):
    await service.delete(category_id)
