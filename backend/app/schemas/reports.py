from pydantic import BaseModel

class EmployeeReportResponse(BaseModel):

    employee_name: str

    total_activities: int

    average_score: float

    best_score: float

    lowest_score: float
