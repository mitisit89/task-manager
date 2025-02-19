from typing import final

from pydantic import BaseModel
from typing import Any
from app.db.enums import TaskStatus, TaskType


class TaskCreate(BaseModel):
    task_type: TaskType
    payload: dict[str, Any]

    @final
    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    payload: dict[str, Any]
    status: TaskStatus


class SuccessResponse(BaseModel):
    status: str


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
