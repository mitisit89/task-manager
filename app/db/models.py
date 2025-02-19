from datetime import datetime
from enum import StrEnum
from sqlmodel import Field, SQLModel


class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class TaskType(StrEnum):
    TYPE_A = "type_a"
    TYPE_B = "type_b"
    TYPE_C = "type_c"


class Tasks(SQLModel, table=True):
    id: int = Field(primary_key=True)
    task_type: TaskType
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    payload: str
    result: str
    error: str
