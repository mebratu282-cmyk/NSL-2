from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Date,
    ForeignKey
)

from app.database.base import Base


class PerformanceResult(Base):
    __tablename__ = "performance_results"

    result_id = Column(
        Integer,
        primary_key=True
    )

    log_activity_id = Column(
        Integer,
        ForeignKey(
            "log_activities.log_activity_id"
        )
    )

    quantity_score = Column(
        Numeric(5, 2)
    )

    time_score = Column(
        Numeric(5, 2)
    )

    quality_score = Column(
        Numeric(5, 2)
    )

    final_score = Column(
        Numeric(5, 2)
    )

    calculated_at = Column(Date)