from typing import Any

from fastapi import Depends

from domain.user.repository import UserDataManagerRepository, UserShowRepository
from domain.user.schema import UserLogin, UserJwtToken, GetUserById
from infrastructure.exceptions.user_exceptions import (
    UserNotFound,
    WrongPassword,
    Unauthorized,
)
from infrastructure.utils.str_helper import convert_to_uuid
from service.auth_handler import AuthHandler


class AuthService:
    def __init__(
        self,
        show_repo: UserShowRepository = Depends(UserShowRepository),
        data_repo: UserDataManagerRepository = Depends(UserDataManagerRepository),
        auth_repo: AuthHandler = Depends(AuthHandler),
    ):
        self.show_repo = show_repo
        self.data_repo = data_repo
        self.auth_repo = auth_repo

    async def login(self, cmd: UserLogin) -> dict[str, str] | dict[str, Any]:
        user = await self.show_repo.get_user_secret(cmd=cmd)
        if not user:
            raise UserNotFound
        if not await self.auth_repo.verify_password(
            password=cmd.password, salt=cmd.login, encoded_pass=user.password
        ):
            raise WrongPassword
        access_token = await self.auth_repo.encode_token(user.id)
        refresh_token = await self.auth_repo.encode_refresh_token(user.id)
        try:
            await self.data_repo.update_token(
                cmd=UserJwtToken(id=user.id, token=refresh_token)
            )
        except Exception as e:
            return {"error": e}
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

    async def logout(self, refresh_token: str) -> UserJwtToken:
        user_id = await self.auth_repo.decode_refresh_token(token=refresh_token)
        token = await self.show_repo.get_user_token(
            cmd=GetUserById(id=await convert_to_uuid(user_id))
        )
        if not token:
            raise Unauthorized
        if token == refresh_token:
            answer = await self.data_repo.delete_token(
                cmd=GetUserById(id=await convert_to_uuid(user_id))
            )
            return answer
        raise Unauthorized

    async def check_auth(self, refresh_token: str) -> UserJwtToken:
        user_id = await self.auth_repo.decode_token(token=refresh_token)
        exist_token = await self.show_repo.get_user_token(
            cmd=GetUserById(id=await convert_to_uuid(user_id))
        )
        print(refresh_token, exist_token, sep="\n")
        if not exist_token:
            raise Unauthorized
        if exist_token == refresh_token:
            return UserJwtToken(id=user_id, token=exist_token)
        raise Unauthorized

    async def refresh_token(self, refresh_token: str) -> UserJwtToken:
        user_id = await self.auth_repo.decode_refresh_token(token=refresh_token)
        exist_token = await self.show_repo.get_user_token(
            cmd=GetUserById(id=await convert_to_uuid(user_id))
        )
        print(refresh_token, exist_token, sep="\n")
        if not exist_token:
            raise Unauthorized
        if exist_token == refresh_token:
            new_token = await self.auth_repo.refresh_token(refresh_token=refresh_token)
            answer = await self.data_repo.update_token(
                cmd=UserJwtToken(
                    id=await convert_to_uuid(user_id),
                    token=new_token["new_refresh_token"],
                )
            )
            return answer
        raise Unauthorized
