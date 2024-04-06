from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from intouch_group.src.infrastructure.settings.config import group_config


class AlchemyInit:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url=url, echo=False)
        self.session_maker = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def session_scoped(self) -> AsyncGenerator:
        async with self.session_maker() as session:
            yield session
            await session.close()


tempest = AlchemyInit(url=group_config.db_url)
