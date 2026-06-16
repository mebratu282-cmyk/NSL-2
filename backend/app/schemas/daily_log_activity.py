from pydantic import BaseModel
from datetime import datetime


class DailyLogActivityCreate(BaseModel):
    log_id: int
    activity_id: int

    actual_quantity: int

    start_time: datetime
    end_time: datetime

    duration_minutes: int

    quality_percent: float

    remarks: str | None = None