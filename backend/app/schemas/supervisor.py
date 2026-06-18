from pydantic import BaseModel
from datetime import date

class PendingLogResponse(BaseModel):

    log_id: int

    employee_name: str

    service_name: str

    log_date: date

    status: str

class Config:
    from_attributes = True

