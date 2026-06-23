from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.database.base import Base

class Notification(Base):

    __tablename__ = "notifications"

    from sqlalchemy import Sequence

    notification_id = Column(
        Integer,
        Sequence("notifications_seq"),
        primary_key=True
    )

    user_id = Column(Integer)

    title = Column(
        String(200)
    )

    message = Column(
        String(1000)
    )

    is_read = Column(
        String(1),
        default="N"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )