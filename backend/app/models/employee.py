from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from app.database.base import Base
from sqlalchemy.orm import relationship



department = relationship(
    "Department",
    back_populates="employees"
)

daily_logs = relationship(
    "DailyLog",
    back_populates="employee"
)

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(
        Integer,
        primary_key=True,
    )

    employee_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    phone = Column(
        String(20)
    )

    email = Column(
        String(100)
    )

    status = Column(
        String(20),
        default="ACTIVE"
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )
    approved_by = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=True
    )

    approval_comment = Column(
        String(500),
        nullable=True
    )