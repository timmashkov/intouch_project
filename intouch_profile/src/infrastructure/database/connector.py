from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from intouch_profile.src.infrastructure.settings.config import main_config


class AlchemyConnector:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url=url, echo=False)
        self.session_maker = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def enter_session(self) -> AsyncGenerator:
        async with self.session_maker() as session:
            yield session
            await session.close()


tempest = AlchemyConnector(url=main_config.db_url)
