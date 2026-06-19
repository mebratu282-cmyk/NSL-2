from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.database.base import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    audit_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(Integer)

    action = Column(
        String(200)
    )

    details = Column(
        String(500)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )