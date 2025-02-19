import asyncio
import json
from typing import Callable, Any
from aio_pika import connect_robust, IncomingMessage
import aioredis

from app.db.connection import async_session
from app.db.models import Task
from app.tasks import tasks as task_functions
from app.db.enums import TaskStatus
from app.settings import settings


TASK_FUNCTIONS: dict[str, Callable[Any, Any]] = {
    "addition": task_functions.add,
    "multiplication": task_functions.mult,
    "reverse": task_functions.rev,
}


async def process_message(message: IncomingMessage) -> None:
    async with message.process():
        data = json.loads(message.body)
        task_id = data.get("task_id")
        async with async_session() as session:
            task = await session.get(Task, task_id)
            if not task:
                return
            task.status = TaskStatus.IN_PROGRESS
            await session.commit()
            try:
                fn = TASK_FUNCTIONS.get(task.task_type)
                if not fn:
                    raise ValueError("Unknown task type")
                result = await fn(task.params)
                task.result = result
                task.status = TaskStatus.COMPLETED
                redis = await aioredis.from_url("redis://redis")
                await redis.set(f"task:{task_id}", json.dumps(result))
            except Exception as e:
                task.error = str(e)
                task.status = TaskStatus.FAILED
            finally:
                await session.commit()


async def main_worker():
    connection = await connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(settings.TASK_QUEUE, durable=True)
    await queue.consume(process_message)
    print("Worker started, waiting for messages...")
    return connection


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_worker())
    loop.run_forever()
