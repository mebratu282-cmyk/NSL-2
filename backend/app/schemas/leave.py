from pydantic import BaseModel
from datetime import datetime


class LeaveCreate(BaseModel):

    leave_type: str

    start_date: datetime

    end_date: datetime

    reason: str


class LeaveApproval(BaseModel):

    approval_comment: str