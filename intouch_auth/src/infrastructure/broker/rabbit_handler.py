import asyncio
import copy
import pickle
from functools import partial
from typing import Any
from uuid import uuid4

import aio_pika
from aio_pika.message import Message, IncomingMessage

from infrastructure.settings.config import base_config


class BaseMQ:
    def __init__(self, mq_url: str) -> None:
        self.mq_url = mq_url
        self.connection = None
        self.channel = None

    @staticmethod
    def serialize_data(data: Any) -> bytes:
        return pickle.dumps(data)

    @staticmethod
    def deserialize_data(data: bytes) -> Any:
        return pickle.loads(data)


class MessageQueue(BaseMQ):
    async def mq_connect(self):
        self.connection = await aio_pika.connect_robust(self.mq_url)
        self.channel = await self.connection.channel()
        print(f"RabbitMQ connection {self.mq_url} is now available")

    async def mq_close_conn(self):
        print(f"RabbitMQ connection {self.mq_url} has benn closed")
        await self.connection.close()

    async def send_message(self, queue_name: str, data: Any):
        message = Message(
            body=self.serialize_data(data=data),
            content_type="application/social_web",
            correlation_id=str(uuid4()),
        )
        print(f"Message {data} has been sent")
        await self.channel.default_exchange.publish(message, queue_name)

    async def listen_queue(self, func, queue_name: str, auto_delete: bool = False):
        queue = await self.channel.declare_queue(
            queue_name, auto_delete=auto_delete, durable=True
        )
        async with queue.iterator() as que_iter:
            async for message in que_iter:
                await func(message)


class RPC(BaseMQ):
    futures = {}

    @staticmethod
    async def cancel_consumer(queue, consumers):
        for key, val in consumers.items():
            await queue.cancel(key)

    async def on_response(self, message: IncomingMessage):
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)
        await message.ack()

    async def call(self, queue_name: str, **kwargs):

        callback_queue = await self.channel.declare_queue(
            exclusive=True, auto_delete=True, durable=True
        )

        await callback_queue.consume(self.on_response)

        consumers = copy.copy(callback_queue._consumers)

        correlation_id = str(uuid4())

        loop = asyncio.get_event_loop()
        future = loop.create_future()
        self.futures[correlation_id] = future

        await self.channel.default_exchange.publish(
            Message(
                body=self.serialize_data(kwargs),
                content_type="application/json",
                correlation_id=correlation_id,
                reply_to=callback_queue.name,
            ),
            routing_key=queue_name,
            mandatory=True,
        )

        response = await future
        await self.cancel_consumer(callback_queue, consumers)

        return self.deserialize_data(response)

    async def consume_queue(self, func, queue_name: str):
        queue = await self.channel.declare_queue(queue_name)
        await queue.consume(
            partial(self.on_call_message, self.channel.default_exchange, func)
        )

    async def on_call_message(self, exchange, func, message: IncomingMessage):
        payload = self.deserialize_data(message.body)
        try:
            result = await func(**payload)
        except Exception as e:
            result = self.serialize_data(dict(error="error", reason=str(e)))

        result = self.serialize_data(result)

        await exchange.publish(
            Message(body=result, correlation_id=message.correlation_id),
            routing_key=message.reply_to,
        )
        await message.ack()


mq_rpc = RPC(base_config.rabbit_url)
mq_handler = MessageQueue(base_config.rabbit_url)
