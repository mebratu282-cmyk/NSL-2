from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    String,
    DateTime
)

from app.database.base import Base


class DailyLogActivity(Base):
    __tablename__ = "daily_log_activities"

    activity_log_id = Column(
        Integer,
        primary_key=True
    )

    log_id = Column(
        Integer,
        ForeignKey("daily_logs.log_id")
    )

    activity_id = Column(
        Integer,
        ForeignKey(
            "activity_templates.activity_id"
        )
    )

    actual_quantity = Column(Integer)

    start_time = Column(DateTime)

    end_time = Column(DateTime)

    duration_minutes = Column(Integer)

    quality_percent = Column(
        Numeric(5, 2)
    )

    performance_score = Column(
        Numeric(5, 2)
    )

    remarks = Column(
        String(1000)
    )