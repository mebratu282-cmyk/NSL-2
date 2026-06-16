from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    employee_code: str
    full_name: str
    phone: str | None = None
    email: str | None = None
    department_id: int


class EmployeeResponse(BaseModel):
    employee_id: int
    employee_code: str
    full_name: str
    phone: str | None = None
    email: str | None = None
    department_id: int

    class Config:
        from_attributes = True

class EmployeeUpdate(BaseModel):
    employee_code: str
    full_name: str
    phone: str | None = None
    email: str | None = None
    department_id: int