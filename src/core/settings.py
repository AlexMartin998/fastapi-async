from pydantic_settings import BaseSettings
from typing import List
from pydantic import Field, field_validator, ValidationError, ValidationInfo


class Settings(BaseSettings):
    ENV: str = "dev"

    DATABASE_URL: str
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])
    ALLOWED_HOSTS: List[str] = Field(default_factory=lambda: ["*"])

    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    TIMEOUT: int = 60
    KEEP_ALIVE: int = 5
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @field_validator("CORS_ORIGINS", "ALLOWED_HOSTS", mode="before")
    def parse_env_list(cls, value):
        # print('------->', value, type(value), '<-------')
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value or []

    @field_validator("CORS_ORIGINS")
    def validate_cors(cls, value, info: ValidationInfo):
        env = info.data.get("ENV", "dev")
        if env != "dev":
            if "*" in value:
                raise ValueError(
                    "Wildcard CORS not allowed in non-dev environments")
            if not value:
                raise ValueError(
                    "CORS_ORIGINS must be set in non-dev environments")
        return value

    @field_validator("ALLOWED_HOSTS")
    def validate_hosts(cls, value, info: ValidationInfo):
        env = info.data.get("ENV", "dev")
        if env != "dev":
            if "*" in value:
                raise ValueError(
                    "Wildcard hosts not allowed in non-dev environments")
            if not value:
                raise ValueError(
                    "ALLOWED_HOSTS must be set in non-dev environments")
        return value


try:
    settings = Settings()
except ValidationError as e:
    import sys
    print("Error loading settings:", e)
    sys.exit(1)
