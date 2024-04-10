from fastapi import Depends

from intouch_profile.src.infrastructure.broker.kafka_handler import kafka_producer
from intouch_profile.src.infrastructure.exceptions.profile_exceptions import (
    ProfileAlreadyExist,
    ProfileNotFound,
    FriendNotFound,
)
from intouch_profile.src.domain.profile.schema import (
    ProfileReturn,
    GetProfileById,
    GetProfileByFirstName,
    GetProfileByLastName,
    CreateProfile,
    UpdateProfile,
    FriendSchema,
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
        if answer:
            return answer
        raise ProfileNotFound

    async def get_profile_by_first_name(
        self, cmd: GetProfileByFirstName
    ) -> ProfileReturn:
        answer = await self.repository.get_profile_by_first_name(cmd=cmd)
        if answer:
            return answer
        raise ProfileNotFound

    async def get_profile_by_last_name(
        self, cmd: GetProfileByLastName
    ) -> ProfileReturn:
        answer = await self.repository.get_profile_by_last_name(cmd=cmd)
        if answer:
            return answer
        raise ProfileNotFound


class ProfileDataManagerService:
    def __init__(
        self,
        repository: ProfileDataManagerRepository = Depends(
            ProfileDataManagerRepository
        ),
        get_data_repo: ProfileShowService = Depends(ProfileShowService),
    ):
        self.repository = repository
        self.get_data_repo = get_data_repo

    async def make_friend(self, cmd: FriendSchema) -> dict[str:str]:
        if not await self.get_data_repo.get_profile_by_id(
            cmd=GetProfileById(id=cmd.profile_id)
        ):
            raise ProfileNotFound
        if not await self.get_data_repo.get_profile_by_id(
            cmd=GetProfileById(id=cmd.friend_id)
        ):
            raise FriendNotFound
        return await self.repository.add_friends(cmd=cmd)

    async def unfriend(self, cmd: FriendSchema) -> dict[str:str]:
        if not await self.get_data_repo.get_profile_by_id(
            cmd=GetProfileById(id=cmd.profile_id)
        ):
            raise ProfileNotFound
        if not await self.get_data_repo.get_profile_by_id(
            cmd=GetProfileById(id=cmd.friend_id)
        ):
            raise FriendNotFound
        return await self.repository.delete_friends(cmd=cmd)

    async def update_profile(
        self, cmd: UpdateProfile, data: GetProfileById
    ) -> ProfileReturn:
        answer = await self.repository.update_profile(cmd=cmd, data=data)
        return answer

    async def delete_profile(self, cmd: GetProfileById) -> ProfileReturn:
        answer = await self.repository.delete_profile(cmd=cmd)
        await kafka_producer.publish_message("delete_user", answer)
        return answer
