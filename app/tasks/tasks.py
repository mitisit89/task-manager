import asyncio

from app.db.models import Task
from app.db.connection import async_session
from app.db.enums import TaskStatus


async def check_cancellation(task_id: int):
    async with async_session() as session:
        task = await session.get(Task, task_id)
        if task and task.status == TaskStatus.CANCELED:
            raise asyncio.CancelledError("Задача была отменена")


async def add(task_id, params: dict[str, int]) -> dict[str, int]:
    a = params.get("a", 0)
    b = params.get("b", 0)
    total_time = 60
    step = 0.5
    elapsed = 0
    while elapsed < total_time:
        await asyncio.sleep(step)
        await check_cancellation(task_id)
        elapsed += step
    return {"result": a + b}


async def mult(task_id, params: dict[str, int]) -> dict[str, int]:
    a = params.get("a", 1)
    b = params.get("b", 1)
    total_time = 60
    step = 0.5
    elapsed = 0
    while elapsed < total_time:
        await asyncio.sleep(step)
        await check_cancellation(task_id)
        elapsed += step
    return {"result": a * b}


async def rev(task_id, params: dict[str, str]) -> dict[str, str]:
    text = params.get("text", "")
    total_time = 60
    step = 0.5
    elapsed = 0
    while elapsed < total_time:
        await asyncio.sleep(step)
        await check_cancellation(task_id)
        elapsed += step
    return {"result": text[::-1]}
