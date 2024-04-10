import pickle
from typing import Any

from intouch_profile.src.infrastructure.broker.kafka_handler import kafka_consumer
from intouch_profile.src.infrastructure.database.db_helper import create_profile_hidden


async def catch_data(message: Any) -> list[Any]:
    inner_storage = []
    part = pickle.loads(message.body)
    if part not in inner_storage:
        inner_storage.append(part)
    print(inner_storage)
    return inner_storage


async def consume_background():
    await kafka_consumer.subscribe_to_topic()
    try:
        while True:
            await kafka_consumer.poll_messages(create_profile_hidden)
    except Exception as e:
        print(e)
