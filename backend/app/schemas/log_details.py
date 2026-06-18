from pydantic import BaseModel

class LogDetailResponse(BaseModel):

    activity_name: str

    quantity_completed: int

    duration_minutes: int

    quality_percent: float

    final_score: float

class Config:
    from_attributes = True
