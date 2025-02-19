from datetime import datetime
from enum import StrEnum
from sqlmodel import Field, SQLModel
from app.db.enums import TaskType, TaskStatus


class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    task_type: TaskType
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    payload: str
    result: str = Field(default=None)
    error: str = Field(default=None)
