from pydantic import BaseModel


class KPICreate(BaseModel):

    kpi_name: str

    description: str

    target_value: int


class KPIAssignment(BaseModel):

    user_id: int

    kpi_id: int