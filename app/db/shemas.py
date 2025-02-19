from typing import final

from pydantic import BaseModel

from app.db.enums import TaskStatus, TaskType


class TaskBase(BaseModel):
    type: TaskType
    payload: str | None = None


class TaskCreate(TaskBase): ...


class TaskUpdate(BaseModel):
    payload: str | None = None
    status: TaskStatus


class TaskResponse(BaseModel):
    id: int
    task_type: TaskType
    status: TaskStatus
    payload: str
    result: str
    error: str

    @final
    class Config:
        from_attributes = True
