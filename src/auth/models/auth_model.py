from typing import List, Optional
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field, Relationship, Table, Column
from sqlalchemy import ForeignKey
import datetime

from src.core.shared.models.audit_mixin_model import AuditMixinModel


# ### Authorization models -----------------
class RefreshToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jti: str = Field(index=True, unique=True)
    user_id: int = Field(foreign_key="user.id")
    expires_at: datetime.datetime
    revoked: bool = Field(default=False)

    # Relacion inversa a User
    user: Optional["User"] = Relationship(back_populates="refresh_tokens")


# ### Authorization models -----------------
# M2M tables -------
user_role = Table(
    "user_role_link", SQLModel.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True),
)
role_perm = Table(
    "role_perm_link", SQLModel.metadata,
    Column("role_id", ForeignKey("role.id"), primary_key=True),
    Column("perm_id", ForeignKey("permission.id"), primary_key=True),
)


# permission ------
class PermissionBase(SQLModel):
    name: str = Field(index=True, max_length=100)


class Permission(AuditMixinModel, PermissionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, index=True, unique=True)

    # Relacion inversa a Role
    roles: List["Role"] = Relationship(
        back_populates="permissions",
        link_model=role_perm,
    )


# role --------------------
class RoleBase(SQLModel):
    name: str = Field(index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
    code: Optional[str] = Field(
        default=None, max_length=200, sa_column_kwargs={"unique": True})


class Role(AuditMixinModel, RoleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, index=True, unique=True)

    # Relacion a Permission
    permissions: List[Permission] = Relationship(
        back_populates="roles",
        link_model=role_perm,
    )
    # Relacion inversa a User
    users: List["User"] = Relationship(
        back_populates="roles",
        link_model=user_role,
    )


# user --------------------
class UserBase(SQLModel):
    username: str = Field(index=True, max_length=50)
    email: str = Field(index=True, max_length=100)
    hashed_password: str
    is_active: bool = Field(default=True)


class User(AuditMixinModel, UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, index=True, unique=True)

    # Relacion a Role
    roles: List[Role] = Relationship(
        back_populates="users",
        link_model=user_role,
    )
    # Relacion a los refresh tokens
    refresh_tokens: List[RefreshToken] = Relationship(back_populates="user")
