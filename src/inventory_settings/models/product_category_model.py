from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from typing import Optional

from src.core.shared.models.audit_mixin_model import AuditMixinModel


class ProductCategoryBase(SQLModel):
    name: str = Field(index=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
    code: Optional[str] = Field(
        default=None,
        max_length=200,
        sa_column_kwargs={"unique": True}
    )


class ProductCategory(AuditMixinModel, ProductCategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(
        default_factory=uuid4,
        index=True,
        nullable=False,
        sa_column_kwargs={"unique": True}
    )
