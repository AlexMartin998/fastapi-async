from src.core.shared.exceptions.custom_exception import CustomException
import re
from passlib.context import CryptContext
from src.core.settings import settings
import uuid
import jwt

from datetime import datetime, timedelta, timezone
datetime.now(timezone.utc)

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OWASP: 8–64 chars, minúsculas, mayúsculas, dígitos y símbolos :contentReference[oaicite:12]{index=12}
# PASSWORD_REGEX = re.compile(
#     r"^(?=.{8,64}$)(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[ !\"#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~]).+$"
# )


class SecurityStaticHelper:

    PASSWORD_REGEX = re.compile(
        r"^(?=.{8,64}$)(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[ !\"#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~]).+$"
    )

    @staticmethod
    def validate_password(password: str):
        if not SecurityStaticHelper.PASSWORD_REGEX.match(password):
            raise CustomException(
                "La contraseña debe tener 8-64 caracteres, incluir mayúsculas, minúsculas, dígitos y símbolos"
            )

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_ctx.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_ctx.verify(plain, hashed)

    @staticmethod
    def create_access_token(sub: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "iss": settings.PROJECT_NAME, "sub": sub, "iat": now,
            "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    async def create_refresh_token(sub: str, repo) -> str:
        now = datetime.now(timezone.utc)
        jti = str(uuid.uuid4())
        payload = {
            "iss": settings.PROJECT_NAME, "sub": sub, "iat": now,
            "exp": now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            "jti": jti
        }
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        # Guardar JTI en DB
        await repo.add_refresh_token(
            jti=jti,
            user_sub=sub,
            expires=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        return token
