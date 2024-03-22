from fastapi import Depends

from domain.user.repository import UserShowRepository
from domain.user.schema import UserReturnData, GetUserById, GetUserByLogin
from infrastructure.database.models import User


class UserShowService:
    def __init__(self, repository: UserShowRepository = Depends(UserShowRepository)):
        self.repository = repository

    async def get_all_users(self) -> list[User]:
        answer = await self.repository.get_users()
        return answer

    async def find_user_by_id(self, cmd: GetUserById) -> UserReturnData:
        answer = await self.repository.get_user_by_id(cmd=cmd)
        return answer

    async def find_user_by_login(self, cmd: GetUserByLogin) -> UserReturnData:
        answer = await self.repository.get_user_by_login(cmd=cmd)
        return answer
