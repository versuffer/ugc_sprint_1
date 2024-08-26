import jwt
from fastapi import Request, status
from jwt import InvalidTokenError

from app.fastapi_app.exeptions import JWTError, auth_error
from app.fastapi_app.services.base import AsyncRequestService
from app.fastapi_app.settings.config import settings


def get_bearer_token(request: Request) -> str:
    if not (token_str := request.headers.get('Authorization')):
        raise auth_error
    try:
        prefix, token = token_str.split(' ')
    except ValueError:
        raise auth_error

    if not prefix == 'Bearer':
        raise auth_error

    return token


class AuthService:
    def __init__(self):
        self.request_service = AsyncRequestService(base_url=settings.AUTH_SERVICE_URL)
        self.verify_token_url = settings.AUTH_SERVICE_API['verify_token']
        self.external_services = settings.SERVICES
        self.user_id_field = settings.USER_ID_FIELD

    async def verify_user_token(self, token: str) -> None:
        """Проверка валидности токена пользователя во внешнем сервисе аутентификации."""
        response = await self.request_service.request(
            url=self.verify_token_url, method='POST', headers={'Authorization': token}
        )
        if not (
            response.status_code == status.HTTP_200_OK and response.json() == {'detail': 'Successful verification'}
        ):
            raise auth_error

    def is_service_authorized(self, service_name: str) -> bool:
        """Проверяет, может ли сервис присылать запросы в приложение."""
        return bool(service_name in self.external_services)

    def get_user_id(self, token) -> str:
        try:
            payload = jwt.decode(token, options={'verify_signature': False})
            if user_id := payload.get(self.user_id_field):
                return user_id
            raise JWTError(f'В токене отсутствует поле {self.user_id_field}.')
        except InvalidTokenError as error:
            raise JWTError(f'Ошибка получения поля {self.user_id_field} из токена: {error}.')
