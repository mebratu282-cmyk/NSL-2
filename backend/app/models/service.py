from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.database.base import Base


class Service(Base):
    __tablename__ = "services"

    service_id = Column(
        Integer,
        primary_key=True,
    )

    category_id = Column(
        Integer,
        ForeignKey(
            "service_categories.category_id"
        )
    )

    service_name = Column(
        String(300),
        nullable=False
    )

    is_active = Column(
        String(1),
        default="Y"
    )