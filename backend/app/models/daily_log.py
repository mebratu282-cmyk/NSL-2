from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey
)

from app.database.base import Base


class DailyLog(Base):
    __tablename__ = "daily_logs"

    log_id = Column(
        Integer,
        primary_key=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )

    service_id = Column(
        Integer,
        ForeignKey("services.service_id")
    )

    log_date = Column(Date)

    activity_description = Column(
        String(2000)
    )

    start_time = Column(DateTime)

    end_time = Column(DateTime)

    outcome = Column(
        String(2000)
    )

    remark = Column(
        String(1000)
    )

    status = Column(
        String(20)
    )

    created_at = Column(Date)

    activity_location = Column(
        String(300)
    )

    duration_minutes = Column(
        Integer
    )