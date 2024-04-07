from contextlib import asynccontextmanager

from fastapi import FastAPI

from intouch_profile.src.infrastructure.database.db_helper import create_profile_hidden
from intouch_profile.src.infrastructure.utils.data_catcher import catch_data
from intouch_profile.src.infrastructure.broker.rabbit_handler import mq_handler, mq_rpc


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mq_handler.mq_connect()
    mq_rpc.channel = mq_handler.channel
    # await mq_rpc.consume_queue(profile_data.create_profile, "registration")
    await mq_handler.listen_queue(create_profile_hidden, "create_user")
    yield
    await mq_handler.mq_close_conn()
