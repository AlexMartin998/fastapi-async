from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import SQLModel

from src.auth.models.auth_model import UserBase, PermissionBase, RoleBase


# ### RefreshToken schemas -----------------
class RefreshTokenBase(BaseModel):
    jti: str
    expires_at: datetime
    revoked: bool = False


class RefreshTokenCreate(RefreshTokenBase):
    user_id: int


class RefreshTokenRead(RefreshTokenBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# ### Permission schemas -----------------
class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: int
    uuid: UUID

    class Config:
        orm_mode = True


class PermissionUpdate(SQLModel):
    name: Optional[str] = None


# ### Role schemas -----------------
class RoleCreate(RoleBase):
    permission_ids: List[int] = []


class RoleRead(RoleBase):
    id: int
    uuid: UUID
    permissions: List[PermissionRead] = []

    class Config:
        orm_mode = True


class RoleUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    code: Optional[str] = None
    permission_ids: Optional[List[int]] = None


# ### User schemas -----------------
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRead(UserBase):
    id: int
    uuid: UUID
    created_at: datetime
    roles: List[RoleRead] = []

    class Config:
        orm_mode = True


class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role_ids: Optional[List[int]] = None
