import asyncio
import json
from typing import Callable, Any
from aio_pika import connect_robust, IncomingMessage
import redis.asyncio as redis
from app.db.connection import async_session
from app.db.models import Task
from app.tasks import tasks as task_functions
from app.db.enums import TaskStatus, TaskType
from app.settings import settings
from datetime import datetime

TASK_FUNCTIONS: dict[TaskType, Callable[Any, Any]] = {
    TaskType.ADD: task_functions.add,
    TaskType.MULTIPLY: task_functions.mult,
    TaskType.REVERSE: task_functions.rev,
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
            task.started_at = datetime.utcnow()
            await session.commit()
            await session.refresh(task)
            try:
                fn = TASK_FUNCTIONS.get(task.task_type)
                if not fn:
                    raise ValueError("Unknown task type")
                print(task.payload)
                result = await fn(task_id, json.loads(task.payload))
                cache = await redis.from_url(settings.REDIS_URL)
                await cache.set(f"task:{task_id}", json.dumps(result))
                task.result = json.dumps(result)
                task.status = TaskStatus.COMPLETED
                task.finished_at = datetime.utcnow()
            except asyncio.CancelledError as ce:
                task.error = str(ce)
                task.finished_at = datetime.utcnow()
            except Exception as e:
                task.error = str(e) + " --error in update task"
                task.status = TaskStatus.FAILED
                task.finished_at = datetime.utcnow()
            finally:
                await session.commit()


async def main_worker():
    print("Starting worker...")
    print(settings.RABBITMQ_URL)
    print(settings.TASK_QUEUE)
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
