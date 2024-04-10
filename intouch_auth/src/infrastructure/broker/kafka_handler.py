import json
import pickle
from typing import Any, Callable
from uuid import UUID

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from infrastructure.settings.config import base_config


class DataHandler:
    @staticmethod
    async def serialize_data(data: Any) -> bytes:
        return pickle.dumps(data)

    @staticmethod
    async def deserialize_data(data: bytes) -> Any:
        return pickle.loads(data)


class KafkaProducer(DataHandler):
    def __init__(self, bootstrap_servers: str, topics: list) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topics = topics
        self.producer = None

    async def connect_producer(self) -> None:
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        print(f"Kafka producer on {self.bootstrap_servers} is up")
        await self.producer.start()

    async def disconnect_producer(self) -> None:
        print(f"Kafka producer on {self.bootstrap_servers} is down")
        await self.producer.stop()

    async def publish_message(self, topic: str, message: Any):
        await self.producer.send_and_wait(
            topic=topic, value=await self.serialize_data(message)
        )
        print(f"{message} has been sent")


class KafkaConsumer(DataHandler):
    def __init__(self, bootstrap_servers: str, topics: list) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topics = topics
        self.consumer = None

    async def connect_consumer(self) -> None:
        self.consumer = AIOKafkaConsumer(bootstrap_servers=self.bootstrap_servers)
        print(f"Kafka consumer on {self.bootstrap_servers} is up")
        await self.consumer.start()

    async def disconnect_consumer(self) -> None:
        print(f"Kafka consumer on {self.bootstrap_servers} is down")
        await self.consumer.stop()

    async def subscribe_to_topic(self):
        await self.consumer.subscribe(self.topics)

    async def poll_messages(self, func: Callable):
        async for message in self.consumer:
            print(f"consumed:{await self.deserialize_data(message.value)}")
            await func(await self.deserialize_data(message.value))


kafka_producer = KafkaProducer(
    bootstrap_servers=base_config.kafka_url, topics=base_config.topics
)
kafka_consumer = KafkaConsumer(
    bootstrap_servers=base_config.kafka_url, topics=base_config.topics
)
