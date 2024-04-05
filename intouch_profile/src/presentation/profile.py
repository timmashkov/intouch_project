from uuid import UUID

from fastapi import APIRouter, Depends

from intouch_profile.src.infrastructure.database.models import Profile
from intouch_profile.src.domain.profile.schema import (
    ProfileReturn,
    GetProfileById,
    GetProfileByFirstName,
    GetProfileByLastName,
    CreateProfile,
    UpdateProfile,
)
from intouch_profile.src.service.service import (
    ProfileShowService,
    ProfileDataManagerService,
)

profile_router = APIRouter(prefix="/profile")


@profile_router.get("/all", response_model=list[ProfileReturn])
async def show_profiles(
    repository: ProfileShowService = Depends(ProfileShowService),
) -> list[Profile]:
    return await repository.get_profiles()


@profile_router.get("/by_id/{profile_id}", response_model=ProfileReturn)
async def show_profile(
    profile_id: UUID, repository: ProfileShowService = Depends(ProfileShowService)
) -> ProfileReturn:
    return await repository.get_profile_by_id(cmd=GetProfileById(id=profile_id))


@profile_router.get("/by_first_name/{first_name}", response_model=ProfileReturn)
async def show_profile_by_first(
    first_name: str, repository: ProfileShowService = Depends(ProfileShowService)
) -> ProfileReturn:
    return await repository.get_profile_by_first_name(
        cmd=GetProfileByFirstName(first_name=first_name)
    )


@profile_router.get("/by_last_name/{last_name}", response_model=ProfileReturn)
async def show_profile_by_last(
    last_name: str, repository: ProfileShowService = Depends(ProfileShowService)
) -> ProfileReturn:
    return await repository.get_profile_by_last_name(
        GetProfileByLastName(last_name=last_name)
    )


@profile_router.post("/create", response_model=ProfileReturn)
async def create_profile(
    # cmd: CreateUpdateProfile,
    repository: ProfileDataManagerService = Depends(ProfileDataManagerService),
) -> ProfileReturn:
    return await repository.create_profile()


@profile_router.patch("/upd/{profile_id}", response_model=ProfileReturn)
async def upd_profile(
    cmd: UpdateProfile,
    profile_id: UUID,
    repository: ProfileDataManagerService = Depends(ProfileDataManagerService),
) -> ProfileReturn:
    return await repository.update_profile(cmd=cmd, data=GetProfileById(id=profile_id))


@profile_router.delete("/del/{profile_id}", response_model=ProfileReturn)
async def del_profile(
    profile_id: UUID,
    repository: ProfileDataManagerService = Depends(ProfileDataManagerService),
) -> ProfileReturn:
    return await repository.delete_profile(cmd=GetProfileById(id=profile_id))
