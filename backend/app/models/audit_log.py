from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.database.connection import Base


class AuditLog(Base):

    __tablename__ = "AUDIT_LOGS"

    audit_id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(Integer)

    action_type = Column(String(100))

    details = Column(String(2000))

    action_date = Column(
        DateTime,
        default=datetime.utcnow
    )