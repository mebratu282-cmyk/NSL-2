from pydantic import BaseModel


class PerformanceResultResponse(BaseModel):
    log_activity_id: int
    quantity_score: float
    time_score: float
    quality_score: float
    final_score: float