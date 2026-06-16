from pydantic import BaseModel
from datetime import date


class DailyLogCreate(BaseModel):
    user_id: int
    service_id: int
    log_date: date


class DailyLogResponse(BaseModel):
    log_id: int
    user_id: int
    service_id: int
    log_date: date
    status: str

    class Config:
        from_attributes = True