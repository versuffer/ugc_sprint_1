from pathlib import Path
from typing import Annotated, Literal

from pydantic import ClickHouseDsn, DirectoryPath, SecretStr, field_validator
from pydantic_core.core_schema import ValidationInfo
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
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: SecretStr
    CLICKHOUSE_DB: str
    CLICKHOUSE_DSN: ClickHouseDsn | str = ''

    @field_validator('CLICKHOUSE_DSN')
    def build_clickhouse_dsn(cls, value: ClickHouseDsn | None, info: ValidationInfo) -> Annotated[str, ClickHouseDsn]:
        if not value:
            value = ClickHouseDsn.build(
                scheme='clickhouse+native',
                username=info.data['CLICKHOUSE_USER'],
                password=info.data['CLICKHOUSE_PASSWORD'].get_secret_value(),
                host=info.data['CLICKHOUSE_HOST'],
                port=info.data['CLICKHOUSE_PORT'],
                path=f"{info.data['CLICKHOUSE_DB'] or ''}",
            )
        return str(value)

    model_config = SettingsConfigDict(env_file=PROJECT_DIR / '.env')


settings = Settings()
