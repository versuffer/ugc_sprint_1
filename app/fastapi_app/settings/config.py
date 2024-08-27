from pathlib import Path
from typing import Literal

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR: DirectoryPath = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    APP_TITLE: str = 'UGC Srint 1'
    APP_DESCRIPTION: str = 'Default description'
    DEBUG: bool = False
    ENABLE_AUTH: bool = True
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'INFO'
    AUTH_SERVICE_URL: str
    AUTH_SERVICE_API: dict = {'verify_token': '/api/v1/auth/verify/access_token'}
    SERVICES: list[str] = ['front']
    USER_ID_FIELD: str = 'login'
    KAFKA_HOST: str
    KAFKA_PORT: str

    model_config = SettingsConfigDict(env_file=PROJECT_DIR / '.env')


settings = Settings()
