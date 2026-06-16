from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from app.database.base import Base

employees = relationship(
    "Employee",
    back_populates="department"
)

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(
        Integer,
        primary_key=True,
    )

    department_name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    description = Column(
        String(255)
    )