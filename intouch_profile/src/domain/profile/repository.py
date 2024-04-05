from typing import Any

from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from intouch_profile.src.domain.profile.schema import (
    GetProfileById,
    ProfileReturn,
    GetProfileByFirstName,
    GetProfileByLastName,
    CreateProfile,
    UpdateProfile,
)
from intouch_profile.src.infrastructure.database.models import Profile
from intouch_profile.src.infrastructure.database.connector import tempest


class ProfileShowRepository:
    def __init__(self, session: AsyncSession = Depends(tempest.enter_session)):
        self.session = session
        self.model = Profile

    async def get_profiles(self) -> list[Profile]:
        stmt = select(self.model).order_by(self.model.first_name)
        answer = await self.session.execute(stmt)
        result = list(answer.scalars().all())
        return result

    async def get_profile_by_id(self, cmd: GetProfileById) -> ProfileReturn | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_profile_by_first_name(
        self, cmd: GetProfileByFirstName
    ) -> ProfileReturn | None:
        stmt = select(self.model).where(self.model.first_name == cmd.first_name)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_profile_by_last_name(
        self, cmd: GetProfileByLastName
    ) -> ProfileReturn | None:
        stmt = select(self.model).where(self.model.last_name == cmd.last_name)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result


class ProfileDataManagerRepository:
    def __init__(self, session: AsyncSession = Depends(tempest.enter_session)):
        self.session = session
        self.model = Profile

    async def create_profile(self, cmd: CreateProfile | Any) -> ProfileReturn | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.first_name,
                self.model.last_name,
                self.model.occupation,
                self.model.bio,
                self.model.status,
                self.model.created_at,
                self.model.is_active,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_profile(
        self, cmd: UpdateProfile, data: GetProfileById
    ) -> ProfileReturn | None:
        stmt = (
            update(self.model)
            .where(self.model.id == data.id)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.first_name,
                self.model.last_name,
                self.model.occupation,
                self.model.bio,
                self.model.status,
                self.model.created_at,
                self.model.is_active,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_profile(self, cmd: GetProfileById) -> ProfileReturn | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == cmd.id)
            .returning(
                self.model.id,
                self.model.first_name,
                self.model.last_name,
                self.model.occupation,
                self.model.bio,
                self.model.status,
                self.model.created_at,
                self.model.is_active,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
