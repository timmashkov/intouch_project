import json
from typing import Any

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from infrastructure.settings.config import base_config


class DataHandler:
    @staticmethod
    async def serialize_data(data: Any) -> bytes:
        return json.dumps(data).encode("utf-8")

    @staticmethod
    async def deserialize_data(data: bytes) -> Any:
        return json.loads(data)


class KafkaProducer(DataHandler):
    def __init__(self, bootstrap_servers: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)

    async def connect_producer(self) -> None:
        print(f"Kafka producer on {self.bootstrap_servers} is up")
        await self.producer.start()

    async def disconnect_producer(self) -> None:
        print(f"Kafka producer on {self.bootstrap_servers} is down")
        await self.producer.stop()

    async def publish_message(self, topic: str, message: Any):
        await self.producer.send_and_wait(
            topic=topic, value=await self.serialize_data(message)
        )


class KafkaConsumer(DataHandler):
    def __init__(self, bootstrap_servers: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.consumer = AIOKafkaConsumer(bootstrap_servers=self.bootstrap_servers)

    async def connect_consumer(self) -> None:
        print(f"Kafka consumer on {self.bootstrap_servers} is up")
        await self.consumer.start()

    async def disconnect_consumer(self) -> None:
        print(f"Kafka consumer on {self.bootstrap_servers} is down")
        await self.consumer.stop()

    async def subscribe_to_topic(self, topic: str):
        await self.consumer.subscribe([topic])

    async def poll_messages(self):
        async for message in self.consumer:
            print(
                "consumed: ",
                await self.deserialize_data(message.topic),
                await self.deserialize_data(message.partition),
                await self.deserialize_data(message.offset),
                await self.deserialize_data(message.key),
                await self.deserialize_data(message.value),
                await self.deserialize_data(message.timestamp),
            )
            yield await self.deserialize_data(message.key), await self.deserialize_data(
                message.value
            )


kafka_producer = KafkaProducer(base_config.KAFKA_BOOTSTRAP_SERVERS)
kafka_consumer = KafkaConsumer(base_config.KAFKA_BOOTSTRAP_SERVERS)
