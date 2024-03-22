from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.user.schema import (
    GetUserById,
    UserReturnData,
    GetUserByLogin,
    CreateUser,
    UpdateUser,
    UserSecretData,
)
from infrastructure.database.models import User
from infrastructure.database.session import vortex


class UserShowRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_gate)):
        self.session = session
        self.model = User

    async def get_users(self) -> list[User]:
        stmt = select(self.model).order_by(self.model.registered_at)
        answer = await self.session.execute(stmt)
        result = list(answer.scalars().all())
        return result

    async def get_user_by_id(self, cmd: GetUserById) -> UserReturnData | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_user_by_login(self, cmd: GetUserByLogin) -> UserReturnData | None:
        stmt = select(self.model).where(self.model.login == cmd.login)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_user_secret(self, cmd: GetUserByLogin) -> UserSecretData | None:
        """
        Запрос для AuthService
        :param cmd:
        :return:
        """
        stmt = select(
            self.model.id, self.model.login, self.model.password, self.model.email
        ).where(self.model.login == cmd.login)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_user_token(self, cmd: GetUserById) -> str:
        """
        Запрос для AuthService
        :param cmd:
        :return:
        """
        stmt = select(self.model.token).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result


class UserDataManagerRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_gate)):
        self.session = session
        self.model = User

    async def create_user(self, cmd: CreateUser) -> UserReturnData | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.login,
                self.model.email,
                self.model.age,
                self.model.phone_number,
                self.model.is_verified,
                self.model.registered_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_user(
        self, cmd: UpdateUser, model_id: GetUserById
    ) -> UserReturnData | None:
        stmt = (
            update(self.model)
            .where(self.model.id == model_id.id)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.login,
                self.model.email,
                self.model.age,
                self.model.phone_number,
                self.model.is_verified,
                self.model.registered_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_user(self, model_id: GetUserById) -> UserReturnData | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == model_id.id)
            .returning(
                self.model.id,
                self.model.login,
                self.model.email,
                self.model.age,
                self.model.phone_number,
                self.model.is_verified,
                self.model.registered_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
