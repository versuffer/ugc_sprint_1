import requests
from starlette import status

from app.fastapi_app.exeptions import ExternalAuthServiceError
from app.fastapi_app.settings.config import settings


class AuthService:
    def __init__(self):
        self.check_token_url: str = settings.CHECK_TOKEN_URL
        self.external_services: str = settings.SERVICES

    def is_service_authorized(self, service_name: str) -> bool:
        """Проверяет, может ли сервис присылать запросы в приложение."""
        return bool(service_name in self.external_services)

    def get_user_id(self, token) -> str:
        return 'ddd'

    def is_user_token_valid(self, token) -> bool:
        """Проверка валидности токена пользователя во внешнем сервисе аутентификации."""
        try:
            response = requests.post(
                url=self.check_token_url,
                json={'token': token},
                timeout=5,
            )
        except TimeoutError as error:
            raise ExternalAuthServiceError(f'Ошибка проверки токена пользователя: {error}')
        if response.status_code == status.HTTP_200_OK:
            return True
        return False
