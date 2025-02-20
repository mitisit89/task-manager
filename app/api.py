import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select

from fastapi.templating import Jinja2Templates
from app.db.connection import async_session
from app.db.enums import TaskStatus
from app.db.models import Task
from app.db.shemas import SuccessResponse, TaskCreate, TaskResponse, TaskUpdate, TaskInfo
from app.tasks.publisher import publish_task

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/publish-task/", response_model=TaskInfo, status_code=202)
async def create_task(task: TaskCreate) -> TaskInfo:
    """
    avaliable task types: add, multiply, reverse
    for add and mul task payload must be {"a": int, "b": int}
    for rev task payload must be {"text": str}
    """
    try:
        async with async_session() as session:
            new_task = Task(task_type=task.task_type, payload=json.dumps(task.payload), status=TaskStatus.PENDING)
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)
            asyncio.create_task(publish_task(new_task.id))
            return TaskInfo(id=new_task.id, status=new_task.status)
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


@router.put("/update-tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    async with async_session() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.status in (TaskStatus.PENDING, TaskStatus.IN_PROGRESS):
            raise HTTPException(status_code=400, detail="Cannot update completed/failed task")
        if task_update.status is not None:
            task.status = task_update.status
        if task_update.payload is not None:
            task.payload = task_update.payload
        if task_update.task_type is not None:
            task.task_type = task_update.task_type
        await session.commit()
        await session.refresh(task)
        return task


@router.get("/retry-tasks/{task_id}", response_model=SuccessResponse, status_code=202)
async def retry_task(task_id: int):
    async with async_session() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if not task.status in (TaskStatus.CANCELED, TaskStatus.COMPLETED, TaskStatus.FAILED):
            raise HTTPException(status_code=400, detail="Cannot retry running task")
        task.status = TaskStatus.PENDING
        await session.commit()
        await session.refresh(task)
        asyncio.create_task(publish_task(task.id))
        return SuccessResponse(status="success")


@router.post("/tasks/{task_id}/cancel", response_model=SuccessResponse)
async def cancel_task(task_id: int):
    async with async_session() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
            raise HTTPException(status_code=400, detail="Cannot cancel completed/failed task")
        task.status = TaskStatus.CANCELED
        await session.commit()
        await session.refresh(task)
        return SuccessResponse(status="success")


@router.get("/", response_class=HTMLResponse)
async def daashboard(request: Request):
    try:
        async with async_session() as session:
            result = await session.execute(select(Task))
            tasks = result.scalars().all()
            total = len(tasks)
            errors = len([t for t in tasks if t.status == "failed"])
            completed_tasks = [t for t in tasks if t.status == "completed" and t.started_at and t.finished_at]
            avg_time = None
            if completed_tasks:
                times = [(t.finished_at - t.started_at).total_seconds() for t in completed_tasks]
                avg_time = sum(times) / len(times)

            metrics = {
                "total_tasks": total,
                "failed_tasks": errors,
                "avg_execution_time": avg_time,
            }
            recent_tasks = completed_tasks[-10:]
            return templates.TemplateResponse(
                request, name="dashboard.html", context={"metrics": metrics, "tasks": recent_tasks}
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
