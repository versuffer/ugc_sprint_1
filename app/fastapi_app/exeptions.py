from fastapi import HTTPException, status

from app.fastapi_app.constants import DEFAULT_ERROR_MESSAGE


class BaseError(Exception):
    def __init__(self, message=None, *args):
        super().__init__(*args)
        self.message = message or DEFAULT_ERROR_MESSAGE

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message}, args={self.args})"


class AuthServiceError(BaseError):
    pass


class JWTError(BaseError):
    pass


auth_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
