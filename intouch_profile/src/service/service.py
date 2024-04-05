from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from infrastructure.exceptions.profile_exceptions import ProfileAlreadyExist
from intouch_profile.src.infrastructure.broker.rabbit_handler import mq_handler, mq_rpc
from intouch_profile.src.domain.profile.schema import (
    ProfileReturn,
    GetProfileById,
    GetProfileByFirstName,
    GetProfileByLastName,
    CreateProfile,
    UpdateProfile,
)
from intouch_profile.src.domain.profile.repository import (
    ProfileShowRepository,
    ProfileDataManagerRepository,
)

from intouch_profile.src.infrastructure.database.models import Profile


class ProfileShowService:
    def __init__(
        self, repository: ProfileShowRepository = Depends(ProfileShowRepository)
    ):
        self.repository = repository

    async def get_profiles(self) -> list[Profile]:
        answer = await self.repository.get_profiles()
        return answer

    async def get_profile_by_id(self, cmd: GetProfileById) -> ProfileReturn:
        answer = await self.repository.get_profile_by_id(cmd=cmd)
        return answer

    async def get_profile_by_first_name(
        self, cmd: GetProfileByFirstName
    ) -> ProfileReturn:
        answer = await self.repository.get_profile_by_first_name(cmd=cmd)
        return answer

    async def get_profile_by_last_name(
        self, cmd: GetProfileByLastName
    ) -> ProfileReturn:
        answer = await self.repository.get_profile_by_last_name(cmd=cmd)
        return answer


class ProfileDataManagerService:
    def __init__(
        self,
        repository: ProfileDataManagerRepository = Depends(
            ProfileDataManagerRepository
        ),
    ):
        self.repository = repository

    async def create_profile(self, cmd: CreateProfile) -> ProfileReturn:
        try:
            answer = await self.repository.create_profile(cmd=cmd)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise ProfileAlreadyExist

    async def update_profile(
        self, cmd: UpdateProfile, data: GetProfileById
    ) -> ProfileReturn:
        answer = await self.repository.update_profile(cmd=cmd, data=data)
        return answer

    async def delete_profile(self, cmd: GetProfileById) -> ProfileReturn:
        answer = await self.repository.delete_profile(cmd=cmd)
        return answer
