from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):

    assigned_to: int

    title: str

    description: str

    due_date: datetime


class TaskStatusUpdate(BaseModel):

    status: str