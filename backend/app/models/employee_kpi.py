from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime

from datetime import datetime

from app.database.connection import Base


class EmployeeKPI(Base):

    __tablename__ = "employee_kpis"

    employee_kpi_id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    kpi_id = Column(
        Integer,
        nullable=False
    )

    current_value = Column(
        Integer,
        default=0
    )

    assigned_date = Column(
        DateTime,
        default=datetime.utcnow
    )