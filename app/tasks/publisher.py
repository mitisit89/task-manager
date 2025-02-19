import json

import aio_pika

from app.settings import settings


async def publish_task(task_id: int):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        message_body = json.dumps({"task_id": task_id}).encode()
        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body),
            routing_key=settings.TASK_QUEUE,
        )
