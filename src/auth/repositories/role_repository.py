from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.shared.repositories.generic_repository import GenericRepository
from src.auth.models.auth_model import Role, role_perm
from src.auth.schemas.auth_schemas import RoleCreate, RoleUpdate


class RoleRepository(GenericRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(Role, session)

    async def create_with_permissions(self, dto: RoleCreate) -> Role:
        role = Role(**dto.model_dump(exclude={"permission_ids"}))
        self.session.add(role)
        await self.session.flush()

        if dto.permission_ids:
            await self.session.execute(
                role_perm.insert().values([
                    {"role_id": role.id, "perm_id": pid}
                    for pid in dto.permission_ids
                ])
            )

        return role

    async def update_with_permissions(self, role_id: int, dto: RoleUpdate) -> Role:
        role = await self.session.get(Role, role_id)
        if not role:
            raise ValueError(f"Role {role_id} no encontrado")

        # apply all non-None, non-permission_ids fields
        for field, val in dto.model_dump(
            exclude_unset=True,
            exclude={"permission_ids"}
        ).items():
            setattr(role, field, val)

        if dto.permission_ids is not None:
            # remove existing links
            await self.session.execute(
                role_perm.delete().where(role_perm.c.role_id == role_id)
            )
            # re-create if any
            if dto.permission_ids:
                await self.session.execute(
                    role_perm.insert().values([
                        {"role_id": role_id, "perm_id": pid}
                        for pid in dto.permission_ids
                    ])
                )

        return role
