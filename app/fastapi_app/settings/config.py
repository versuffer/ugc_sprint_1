from pathlib import Path
from pprint import pformat
from typing import Literal


from pydantic import DirectoryPath
from pydantic_settings import BaseSettings

PROJECT_DIR: DirectoryPath = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    APP_TITLE: str
    APP_DESCRIPTION: str
    API_V1_STR: str
    DEBUG: bool
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'INFO'
    SQL_LOGS: bool = False
    CHECK_TOKEN_URL: str
    SERVICES: list[str]

    ROOT_DIR: DirectoryPath = Path(__file__).resolve().parent.parent

    class Config:
        env_file = PROJECT_DIR / '.env'
        case_sensitive = True

    def __repr__(self):
        return pformat(self.dict())

    def __str__(self):
        return self.__repr__()


settings = Settings()
