from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Date,
    Numeric
)

from app.database.base import Base


class LogActivity(Base):
    __tablename__ = "log_activities"

    log_activity_id = Column(
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

    quantity_completed = Column(
        Integer
    )

    duration_minutes = Column(
        Integer
    )

    quality_percent = Column(
        Numeric(5, 2)
    )

    created_at = Column(Date)