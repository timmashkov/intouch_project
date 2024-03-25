from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.broker.kafka_handler import kafka_producer, kafka_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_producer.connect_producer()
    await kafka_consumer.connect_consumer()
    yield
    await kafka_producer.disconnect_producer()
    await kafka_consumer.disconnect_consumer()
