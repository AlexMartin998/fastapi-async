from fastapi import APIRouter, Query, status, Depends
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



@router.get("/", response_model=List[ProductCategoryRead])
async def list_categories(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, le=200),
    service: CategoryService = Depends(get_category_service),
):
    return await service.find_all(offset, limit)


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
