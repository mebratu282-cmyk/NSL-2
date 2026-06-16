from pydantic import BaseModel


class ServiceCategoryCreate(BaseModel):
    category_name: str