from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from sqlalchemy import select, and_
from src.auth.models.auth_model import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, jti: str, user_id: int, expires: datetime) -> RefreshToken:
        token = RefreshToken(jti=jti, user_id=user_id, expires_at=expires)
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_valid(self, jti: str) -> RefreshToken | None:
        now = datetime.now(datetime.timezone.utc)
        stmt = select(RefreshToken).where(
            and_(
                RefreshToken.jti == jti,
                RefreshToken.revoked.is_(False),
                RefreshToken.expires_at > now
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke(self, jti: str) -> None:
        token = await self.get_valid(jti)
        if token:
            token.revoked = True
            await self.session.flush()
