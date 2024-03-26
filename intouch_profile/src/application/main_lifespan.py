from contextlib import asynccontextmanager

from fastapi import FastAPI

from intouch_profile.src.infrastructure.broker.kafka_handler import (
    kafka_producer,
    kafka_consumer,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await kafka_producer.connect_producer()
    await kafka_consumer.connect_consumer()
    await kafka_consumer.poll_messages()
    yield
    # await kafka_producer.disconnect_producer()
    await kafka_consumer.disconnect_consumer()
