from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
import sqlalchemy as sa


def utcnow_py():
    # fallback en memoria/tests; DB pone su default
    return datetime.now(timezone.utc)


class AuditMixinModel(SQLModel):
    created_at: datetime = Field(
        default_factory=utcnow_py,
        nullable=False,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.text("timezone('utc', now())")},
    )
    updated_at: datetime = Field(
        default_factory=utcnow_py,
        nullable=False,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.text("timezone('utc', now())")},
    )
