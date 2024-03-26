import json
from typing import Any

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from intouch_profile.src.infrastructure.settings import main_config


class DataDumper:
    @staticmethod
    async def serialize_data(data: Any) -> bytes:
        return json.dumps(data).encode("utf-8")

    @staticmethod
    async def deserialize_data(data: bytes) -> Any:
        return json.loads(data)


class AIOProducer(DataDumper):
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
        if topic in self.topics:
            await self.producer.send_and_wait(
                topic=topic, value=await self.serialize_data(message)
            )
        raise NameError("Wrong topic name")


class AIOConsumer(DataDumper):
    def __init__(self, bootstrap_servers: str, topics: list) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topics = topics
        self.consumer = None

    async def connect_consumer(self) -> None:
        self.consumer = AIOKafkaConsumer(
            main_config.TOPIC_REG,
            bootstrap_servers=self.bootstrap_servers,
            group_id="my_consumer_group",
            auto_offset_reset="earliest",
        )
        print(f"Kafka consumer on {self.bootstrap_servers} is up")
        await self.consumer.start()

    async def disconnect_consumer(self) -> None:
        print(f"Kafka consumer on {self.bootstrap_servers} is down")
        await self.consumer.stop()

    async def subscribe_to_topic(self):
        await self.consumer.subscribe(self.topics)

    async def poll_messages(self):
        async for message in self.consumer:
            print(f"consumed:{await self.deserialize_data(message.value)}")


kafka_producer = AIOProducer(
    bootstrap_servers=main_config.kafka_url, topics=main_config.topics
)
kafka_consumer = AIOConsumer(
    bootstrap_servers=main_config.kafka_url, topics=main_config.topics
)
