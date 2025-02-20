from pydantic import BaseModel, validator, Json, ConfigDict, with_config
from typing import Any
from app.db.enums import TaskStatus, TaskType
from datetime import datetime


class TaskCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    task_type: TaskType
    payload: dict[str, Any]


class TaskUpdate(BaseModel):
    payload: dict[str, Any]
    status: TaskStatus


class SuccessResponse(BaseModel):
    status: str


class TaskInfo(BaseModel):
    id: int
    status: TaskStatus


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    task_type: TaskType
    status: TaskStatus
    payload: Json[Any]
    result: str | None
    error: str | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
