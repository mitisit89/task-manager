import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select

from app.db.connection import async_session
from app.db.enums import TaskStatus
from app.db.models import Task
from app.db.shemas import SuccessResponse, TaskCreate, TaskResponse, TaskUpdate
from app.tasks.publisher import publish_task

router = APIRouter()


@router.post("/publish-task/", response_model=SuccessResponse, status_code=201)
async def create_task_async(task: TaskCreate):
    try:
        async with async_session() as session:
            new_task = Task(task_type=task.task_type, payload=json.dumps(task.payload), status="pending")
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)
            print(new_task.id)
            asyncio.create_task(publish_task(new_task.id))
            return SuccessResponse(status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    async with async_session() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task


@router.get("/tasks", response_model=list[TaskResponse])
async def list_tasks(status: str | None = None, task_type: str | None = None):
    async with async_session() as session:
        query = select(Task)
        if status:
            query = query.where(Task.status == status)
        if task_type:
            query = query.where(Task.task_type == task_type)
        result = await session.execute(query)
        tasks = result.scalars().all()
        return tasks


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    async with async_session() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task_update.payload is not None:
            task.payload = task_update.payload
        if task_update.task_type is not None:
            task.task_type = task_update.task_type
        await session.commit()
        await session.refresh(task)
        return task


@router.post("/tasks/{task_id}/cancel", response_model=SuccessResponse)
async def cancel_task(task_id: int):
    async with async_session() as session:
        task = await session.get(Task, task_id)
        print(task.status)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
            raise HTTPException(status_code=400, detail="Cannot cancel completed/failed task")
        task.status = TaskStatus.CANCELED
        await session.commit()
        await session.refresh(task)
        return SuccessResponse(status="success")


@router.get("/metrics", response_model=None)
async def get_metrics(session=Depends(async_session)):
    all_tasks_result = await session.execute(select(Task))
    tasks = all_tasks_result.scalars().all()
    total = len(tasks)
    errors = len([t for t in tasks if t.status == TaskStatus.FAILED])
    completed_tasks = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
    cancelled_tasks = len([t for t in tasks if t.status == TaskStatus.CANCELED])
    return {
        "total_tasks": total,
        "failed_tasks": errors,
        "completed_tasks": completed_tasks,
        "cancelled_tasks": cancelled_tasks,
    }


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    html_content = """
    <html>
        <head>
            <title>Task Dashboard</title>
        </head>
        <body>
            <h1>Task Metrics</h1>
            <p>Получите JSON-метрики через <a href="/metrics">/metrics</a></p>
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)
