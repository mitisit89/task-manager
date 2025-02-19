from pydantic import BaseModel
from datetime import datetime
from enum import StrEnum


class TaskStatus(StrEnum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class TaskCreate(BaseModel):
    name: str
    description: str | None = None
    type: str


class TaskResponse(TaskCreate):
    id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime


class TaskUpdate(BaseModel):
    status: TaskStatus
    result: str | None = None
