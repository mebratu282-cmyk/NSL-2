from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.database.connection import Base


class KPI(Base):

    __tablename__ = "kpis"

    kpi_id = Column(
        Integer,
        primary_key=True
    )

    kpi_name = Column(
        String(200),
        nullable=False
    )

    description = Column(
        String(1000)
    )

    target_value = Column(
        Integer
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )