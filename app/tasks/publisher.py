import aio_pika
from app.settings import settings
import json


async def publish_task(task_id: int | None):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        message_body = json.dumps({"task_id": task_id}).encode()
        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body),
            routing_key=settings.TASK_QUEUE,
        )
