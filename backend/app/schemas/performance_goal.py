from pydantic import BaseModel
from datetime import datetime

class GoalCreate(BaseModel):

    user_id: int

    target_score: int

    period: str

    start_date: datetime

    end_date: datetime