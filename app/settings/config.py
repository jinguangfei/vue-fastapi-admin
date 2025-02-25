import os
import typing
import json
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="",
        validate_assignment=True,
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow'
    )
    
    # 基础配置
    VERSION: str = "1.0.0"
    APP_TITLE: str = "FastAPI Boilerplate"
    PROJECT_NAME: str = "fastapi-boilerplate"
    APP_DESCRIPTION: str = "FastAPI Boilerplate"

    # CORS配置
    CORS_ORIGINS: typing.List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: typing.List[str] = ["*"]
    CORS_ALLOW_HEADERS: typing.List[str] = ["*"]

    DEBUG: bool = True

    # 路径配置
    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(BASE_DIR, "app/logs")

    # JWT配置
    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # 数据库配置
    @property
    def TORTOISE_ORM(self) -> dict:
        connections = {
            "sqlite": {
                "engine": "tortoise.backends.sqlite",
                "credentials": {"file_path": f"{self.BASE_DIR}/db.sqlite3"},
            }
        }
        
        return {
            "connections": connections,
            "apps": {
                "models": {
                    "models": ["app.models", "aerich.models"],
                    "default_connection": "sqlite",
                },
            },
            "use_tz": False,
            "timezone": "Asia/Shanghai",
        }

    DATETIME_FORMAT: str

    # Redis配置
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str
    REDIS_MAX_CONNECTIONS: int = 100


settings = Settings()