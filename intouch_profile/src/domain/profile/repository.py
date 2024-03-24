from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.profile.schema import GetProfileById
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

    async def get_profile_by_id(self, cmd: GetProfileById):
        pass
