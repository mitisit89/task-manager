from enum import StrEnum


class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class TaskType(StrEnum):
    ADD = "add"
    MULTIPLY = "multiply"
    REVERSE = "reverse"
