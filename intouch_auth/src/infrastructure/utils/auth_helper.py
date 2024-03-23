from fastapi import Security
from fastapi.security import HTTPBearer, APIKeyHeader, HTTPAuthorizationCredentials

from domain.user.schema import UserAccessToken
from infrastructure.exceptions.token_exceptions import InvalidCredentials
from infrastructure.exceptions.user_exceptions import Unauthorized
from infrastructure.settings.config import base_config
from service.auth_handler import AuthHandler

jwt_header = HTTPBearer()

api_x_key_header = APIKeyHeader(name="X_ACCESS_TOKEN")

auth_handler = AuthHandler()


async def get_token_key(
    api_key_header: str = Security(api_x_key_header),
):
    value = base_config.X_API_TOKEN
    if api_key_header != value:
        raise InvalidCredentials


async def check_jwt(credentials: HTTPAuthorizationCredentials = Security(jwt_header)):
    token = credentials.credentials
    if not await auth_handler.decode_token(token):
        raise Unauthorized
    return UserAccessToken(access_token=token)
