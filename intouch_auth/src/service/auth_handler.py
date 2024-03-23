from datetime import datetime
from uuid import UUID

from infrastructure.exceptions.token_exceptions import (
    InvalidScopeToken,
    TokenExpired,
    InvalidToken,
    RefreshTokenExpired,
    InvalidRefreshToken,
)
from infrastructure.settings.config import base_config

import hashlib
import json
import jwt


class AuthHandler:
    secret = base_config.SECRET

    @staticmethod
    async def encode_pass(password: str, salt: str) -> str:
        password = password.encode("utf-8")
        salt = salt.encode("utf-8")
        hashed_pass = hashlib.pbkdf2_hmac(
            "sha256", password=password, salt=salt, iterations=1000
        )
        return hashed_pass.hex()

    async def verify_password(
        self, password: str, salt: str, encoded_pass: str
    ) -> bool:
        hashed_password = await self.encode_pass(password=password, salt=salt)
        return hashed_password == encoded_pass

    async def encode_token(self, user_id: UUID) -> str:
        expiration = 3600
        payload = {
            "expiration": int(datetime.now().timestamp() + expiration),
            "iat": int(datetime.now().timestamp()),
            "scope": "access_token",
            "sub": json.dumps(user_id, default=str),
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    async def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "refresh_token":
                return payload["sub"]
            raise InvalidScopeToken
        except jwt.ExpiredSignatureError:
            raise TokenExpired
        except jwt.InvalidTokenError:
            raise InvalidToken

    async def encode_refresh_token(self, user_id: UUID | str) -> str:
        expiration = 3600
        payload = {
            "expiration": int(datetime.now().timestamp() + expiration),
            "iat": int(datetime.now().timestamp()),
            "scope": "refresh_token",
            "sub": json.dumps(user_id, default=str),
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    async def decode_refresh_token(self, token: str) -> str:
        payload = jwt.decode(token, self.secret, algorithms=["HS256"])
        if payload["scope"] == "refresh_token":
            return payload["sub"]
        raise InvalidScopeToken

    async def refresh_token(self, refresh_token: str) -> dict[str, str]:
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "refresh_token":
                user_id = payload["sub"]
                new_token = await self.encode_token(user_id)
                new_refresh = await self.encode_refresh_token(user_id)
                return {"new_access_token": new_token, "new_refresh_token": new_refresh}
            raise InvalidScopeToken
        except jwt.ExpiredSignatureError:
            raise RefreshTokenExpired
        except jwt.InvalidTokenError:
            raise InvalidRefreshToken
