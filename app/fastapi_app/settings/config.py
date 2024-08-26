from pathlib import Path
from pprint import pformat
from typing import Literal

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings

PROJECT_DIR: DirectoryPath = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    APP_TITLE: str
    APP_DESCRIPTION: str
    DEBUG: bool
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'INFO'
    SQL_LOGS: bool = False
    AUTH_SERVICE_URL: str
    AUTH_SERVICE_API: dict = {'verify_token': '/api/v1/auth/verify/access_token'}
    SERVICES: list[str] = ['front']
    USER_ID_FIELD: str = 'login'
    KAFKA_HOST: str
    KAFKA_PORT: str
    ROOT_DIR: DirectoryPath = Path(__file__).resolve().parent.parent

    class Config:
        env_file = PROJECT_DIR / '.env'
        case_sensitive = True

    def __repr__(self):
        return pformat(self.dict())

    def __str__(self):
        return self.__repr__()


settings = Settings()
