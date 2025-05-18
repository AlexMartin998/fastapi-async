from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = False
    DATABASE_URL: str
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    TIMEOUT: int = 60
    KEEP_ALIVE: int = 5
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Config()
