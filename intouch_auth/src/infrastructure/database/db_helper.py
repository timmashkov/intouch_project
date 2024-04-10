from sqlalchemy import delete

from infrastructure.database.models import User
from infrastructure.database.session import vortex


async def delete_user_hidden(data):
    print(data)
    async with vortex.engine.connect() as session:
        stmt = (
            delete(User)
            .where(User.id == data["user_id"])
            .returning(
                User.id,
                User.login,
                User.email,
                User.age,
                User.phone_number,
                User.is_verified,
                User.registered_at,
            )
        )
        answer = await session.execute(stmt)
        await session.commit()
        result = answer.mappings().first()
        print(result)
        return result
