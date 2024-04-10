from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.user.repository import UserShowRepository, UserDataManagerRepository
from domain.user.schema import (
    UserReturnData,
    GetUserById,
    GetUserByLogin,
    CreateUser,
    UpdateUser,
)
from infrastructure.broker.kafka_handler import kafka_producer
from infrastructure.database.models import User
from infrastructure.exceptions.user_exceptions import UserNotFound, UserAlreadyExist
from service.auth_handler import AuthHandler


class UserShowService:
    def __init__(self, repository: UserShowRepository = Depends(UserShowRepository)):
        self.repository = repository

    async def get_all_users(self) -> list[User]:
        answer = await self.repository.get_users()
        return answer

    async def find_user_by_id(self, cmd: GetUserById) -> UserReturnData:
        answer = await self.repository.get_user_by_id(cmd=cmd)
        if not answer:
            raise UserNotFound
        return answer

    async def find_user_by_login(self, cmd: GetUserByLogin) -> UserReturnData:
        answer = await self.repository.get_user_by_login(cmd=cmd)
        if not answer:
            raise UserNotFound
        return answer


class UserDataManagerService:
    def __init__(
        self,
        repository: UserDataManagerRepository = Depends(UserDataManagerRepository),
        auth: AuthHandler = Depends(AuthHandler),
    ) -> None:
        self.repository = repository
        self.auth = auth

    async def register_user(self, cmd: CreateUser) -> UserReturnData:
        try:
            salted_pass = await self.auth.encode_pass(cmd.password, cmd.login)
            data = CreateUser(
                login=cmd.login,
                password=salted_pass,
                email=cmd.email,
                phone_number=cmd.phone_number,
                age=cmd.age,
            )
            answer = await self.repository.create_user(cmd=data)
            await kafka_producer.publish_message("registration", answer)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise UserAlreadyExist

    async def change_user(
        self, cmd: UpdateUser, model_id: GetUserById
    ) -> UserReturnData:
        answer = await self.repository.update_user(cmd=cmd, model_id=model_id)
        if not answer:
            raise UserNotFound
        return answer

    async def drop_user(self, model_id: GetUserById) -> UserReturnData:
        answer = await self.repository.delete_user(model_id=model_id)
        if not answer:
            raise UserNotFound
        return answer
