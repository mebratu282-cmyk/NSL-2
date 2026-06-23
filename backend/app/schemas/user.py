from pydantic import BaseModel


class SupervisorAssignment(
    BaseModel
):
    supervisor_id: int

class UserCreate(BaseModel):
    username: str
    full_name: str
    password: str
    role: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    full_name: str
    role: str

    class Config:
        from_attributes = True