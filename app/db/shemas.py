from typing import final

from pydantic import BaseModel, validator, Json
from typing import Any
from app.db.enums import TaskStatus, TaskType
import json


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
    payload: Json[Any]
    result: str | None
    error: str | None

    @final
    class Config:
        from_attributes = True
