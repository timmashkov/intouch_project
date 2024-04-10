from sqlalchemy import insert

from intouch_profile.src.infrastructure.database.models import Profile
from intouch_profile.src.infrastructure.database.connector import tempest


async def create_profile_hidden(data):
    async with tempest.engine.connect() as session:
        stmt = (
            insert(Profile)
            .values(
                first_name="",
                last_name="",
                user_id=data["id"],
                email=data["email"],
                age=int(data["age"]),
                phone_number=data["phone_number"],
                occupation="",
                status="",
                bio="",
            )
            .returning(
                Profile.id,
                Profile.first_name,
                Profile.last_name,
                Profile.occupation,
                Profile.email,
                Profile.age,
                Profile.phone_number,
                Profile.bio,
                Profile.status,
                Profile.created_at,
                Profile.is_active,
            )
        )
        answer = await session.execute(stmt)
        await session.commit()
        result = answer.mappings().first()
        print(result)
        return result
