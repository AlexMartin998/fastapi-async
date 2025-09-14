from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from src.core.shared.repositories.generic_repository import GenericRepository
from src.auth.models.auth_model import User, user_role


class UserRepository(GenericRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def assign_roles(self, user_id: int, role_ids: List[int]) -> User:
        # limpiar roles existentes
        await self.session.execute(user_role.delete().where(user_role.c.user_id == user_id))
        if role_ids:
            await self.session.execute(
                user_role.insert().values([
                    {"user_id": user_id, "role_id": rid}
                    for rid in role_ids
                ])
            )
        return await self.session.get(User, user_id)

    async def remove_role(self, user_id: int, role_id: int) -> User:
        await self.session.execute(
            user_role.delete().where(
                (user_role.c.user_id == user_id) &
                (user_role.c.role_id == role_id)
            )
        )
        return await self.session.get(User, user_id)
