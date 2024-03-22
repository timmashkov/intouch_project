from uuid import UUID

from fastapi import APIRouter, Depends, status

from domain.user.schema import (
    UserReturnData,
    GetUserById,
    GetUserByLogin,
    CreateUser,
    UpdateUser,
)
from infrastructure.database.models import User
from service.user_service import UserShowService, UserDataManagerService

user_router = APIRouter(prefix="/user")


# get endpoints
@user_router.get("/all", response_model=list[UserReturnData])
async def show_all_users(
    repository: UserShowService = Depends(UserShowService),
) -> list[User]:
    return await repository.get_all_users()


@user_router.get("/search/{user_id}", response_model=UserReturnData)
async def show_user_by_id(
    user_id: UUID, repository: UserShowService = Depends(UserShowService)
) -> UserReturnData:
    return await repository.find_user_by_id(cmd=GetUserById(id=user_id))


@user_router.get("/{login}", response_model=UserReturnData)
async def show_user_by_login(
    login: str, repository: UserShowService = Depends(UserShowService)
) -> UserReturnData:
    return await repository.find_user_by_login(cmd=GetUserByLogin(login=login))


# data manager endpoints
@user_router.post(
    "/", response_model=UserReturnData, status_code=status.HTTP_201_CREATED
)
async def registration(
    cmd: CreateUser,
    repository: UserDataManagerService = Depends(UserDataManagerService),
) -> UserReturnData:
    return await repository.register_user(cmd=cmd)


@user_router.patch("/upd/{user_id}", response_model=UserReturnData)
async def upd_user(
    user_id: UUID,
    cmd: UpdateUser,
    repository: UserDataManagerService = Depends(UserDataManagerService),
) -> UserReturnData:
    return await repository.change_user(cmd=cmd, model_id=GetUserById(id=user_id))


@user_router.delete("/del/{user_id}", response_model=UserReturnData)
async def del_user(
    user_id: UUID, repository: UserDataManagerService = Depends(UserDataManagerService)
) -> UserReturnData:
    return await repository.drop_user(model_id=GetUserById(id=user_id))
