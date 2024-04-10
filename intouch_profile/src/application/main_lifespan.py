import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from intouch_profile.src.infrastructure.broker.kafka_handler import (
    kafka_producer,
    kafka_consumer,
)
from intouch_profile.src.infrastructure.broker.rabbit_handler import mq_handler, mq_rpc
from intouch_profile.src.infrastructure.database.db_helper import create_profile_hidden


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mq_handler.mq_connect()
    mq_rpc.channel = mq_handler.channel
    await kafka_producer.connect_producer()
    await kafka_consumer.connect_consumer()
    asyncio.create_task(kafka_consumer.poll_messages(create_profile_hidden))
    yield
    await mq_handler.mq_close_conn()
    await kafka_producer.disconnect_producer()
    await kafka_consumer.disconnect_consumer()
