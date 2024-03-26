from infrastructure.broker.kafka_handler import DataHandler


class RPC(DataHandler):
    futures = {}

    @staticmethod
    async def cancel_consumer(queue, consumers):
        """
        Удаление из очереди слушателей
        """
        for key, val in consumers.items():
            await queue.cancel(key)

    async def on_response(self, message: IncomingMessage):
        """
        Функция которая обрабатывает приходящий ответ из другого сервиса
        """
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)
        await message.ack()

    async def call(self, queue_name: str, **kwargs):
        """
        RPC-метод для отправки в другой сервис с целью возврата ответа из другого сервиса.
        """
        # Создание уникальной очереди на которую будет возвращен ответ из другого сервиса.
        callback_queue = await self.channel.declare_queue(
            exclusive=True, auto_delete=True, durable=True
        )

        await callback_queue.consume(
            self.on_response
        )  # Метод класса который обрабатывает ответ

        consumers = copy.copy(
            callback_queue._consumers
        )  # Копирование консумеров для удаления очереди из раббита

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
        # Удаление слушателей.
        await self.cancel_consumer(callback_queue, consumers)

        return self.deserialize_data(response)

    async def consume_queue(self, func, queue_name: str):
        """Прослушивание очереди брокера."""
        queue = await self.channel.declare_queue(queue_name)
        await queue.consume(
            partial(self.on_call_message, self.channel.default_exchange, func)
        )

    async def on_call_message(self, exchange, func, message: IncomingMessage):
        """Единая функция для приема message из других сервисов и отправки обратно ответа."""
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
