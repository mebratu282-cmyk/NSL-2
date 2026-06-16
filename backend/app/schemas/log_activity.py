from pydantic import BaseModel


class LogActivityCreate(BaseModel):

    log_id: int

    activity_id: int

    quantity_completed: int

    duration_minutes: int

    quality_percent: float