from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from datetime import datetime

from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(
        Integer,
        primary_key=True,
    )

    employee_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False
    )

    department = Column(
        String(100)
    )

    phone = Column(
        String(20)
    )

    password_hash = Column(
        String(255)
    )

    is_active = Column(
        String(1)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    last_login = Column(
        DateTime
    )

    supervisor_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )