from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey
)

from app.database.base import Base


class Approval(Base):
    __tablename__ = "approvals"

    approval_id = Column(
        Integer,
        primary_key=True
    )

    log_id = Column(
        Integer,
        ForeignKey("daily_logs.log_id")
    )

    approved_by = Column(
        Integer,
        ForeignKey("users.user_id")
    )

    approval_status = Column(
        String(20)
    )

    comments = Column(
        String(1000)
    )

    approval_date = Column(Date)