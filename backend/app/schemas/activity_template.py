from pydantic import BaseModel


class ActivityTemplateCreate(BaseModel):
    service_id: int
    activity_name: str

    standard_quantity: int | None = None
    standard_duration_minutes: int | None = None
    standard_quality_percent: float | None = None