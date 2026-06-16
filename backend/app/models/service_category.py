from sqlalchemy import Column, Integer, String

from app.database.base import Base


class ServiceCategory(Base):
    __tablename__ = "service_categories"

    category_id = Column(
        Integer,
        primary_key=True,
    )

    category_name = Column(
        String(200),
        nullable=False
    )

    is_active = Column(
        String(1),
        default="Y"
    )