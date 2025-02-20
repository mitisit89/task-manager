from datetime import datetime
from enum import StrEnum
from sqlmodel import Field, SQLModel, JSON
from app.db.enums import TaskType, TaskStatus
from typing import Any


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task_type: TaskType
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    payload: str
    result: str | None = None
    error: str | None = None
