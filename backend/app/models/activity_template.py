from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric
)

from app.database.base import Base


class ActivityTemplate(Base):
    __tablename__ = "activity_templates"

    activity_id = Column(
        Integer,
        primary_key=True,
    )

    service_id = Column(
        Integer,
        ForeignKey("services.service_id")
    )

    activity_name = Column(
        String(500)
    )

    standard_quantity = Column(
        Integer
    )

    standard_duration_minutes = Column(
        Integer
    )

    standard_quality_percent = Column(
        Numeric(5, 2)
    )

    is_active = Column(
        String(1),
        default="Y"
    )