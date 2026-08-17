from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "TODO"
    estimate_days: float = 0.0

class TaskCreate(TaskBase):
    project_id: int

class TaskUpdateEstimate(BaseModel):
    estimate_days: float

class Task(TaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int] = None
    started_at: Optional[datetime] = None
    due_date: Optional[datetime] = None

    class Config:
        from_attributes = True
