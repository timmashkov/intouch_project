from fastapi import Depends

from intouch_profile.src.infrastructure.broker.kafka_handler import kafka_consumer
from intouch_profile.src.domain.profile.schema import (
    ProfileReturn,
    GetProfileById,
    GetProfileByFirstName,
    GetProfileByLastName,
    CreateUpdateProfile,
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

    async def create_profile(self, cmd: CreateUpdateProfile) -> ProfileReturn:
        await kafka_consumer.subscribe_to_topic("registration")
        answer = await self.repository.create_profile(cmd=cmd)
        return answer

    async def update_profile(
        self, cmd: CreateUpdateProfile, data: GetProfileById
    ) -> ProfileReturn:
        answer = await self.repository.update_profile(cmd=cmd, data=data)
        return answer

    async def delete_profile(self, cmd: GetProfileById) -> ProfileReturn:
        answer = await self.repository.delete_profile(cmd=cmd)
        return answer
