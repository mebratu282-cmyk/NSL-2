from pydantic import BaseModel


class ServiceCreate(BaseModel):
    category_id: int
    service_name: str