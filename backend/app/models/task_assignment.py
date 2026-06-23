from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.database.connection import Base


class TaskAssignment(Base):

    __tablename__ = "task_assignments"

    task_id = Column(
        Integer,
        primary_key=True
    )

    assigned_by = Column(
        Integer,
        nullable=False
    )

    assigned_to = Column(
        Integer,
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        String(1000)
    )

    due_date = Column(
        DateTime
    )

    status = Column(
        String(20),
        default="PENDING"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )