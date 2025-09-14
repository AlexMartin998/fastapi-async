from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.shared.repositories.generic_repository import GenericRepository
from src.auth.models.auth_model import Permission


class PermissionRepository(GenericRepository[Permission]):
    def __init__(self, session: AsyncSession):
        super().__init__(Permission, session)
