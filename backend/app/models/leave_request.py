from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.database.connection import Base


class LeaveRequest(Base):

    __tablename__ = "leave_requests"

    leave_id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    leave_type = Column(
        String(50)
    )

    start_date = Column(
        DateTime
    )

    end_date = Column(
        DateTime
    )

    reason = Column(
        String(1000)
    )

    status = Column(
        String(20),
        default="PENDING"
    )

    approved_by = Column(
        Integer
    )

    approval_comment = Column(
        String(1000)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )