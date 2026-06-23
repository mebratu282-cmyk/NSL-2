from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from app.database.connection import Base

class PerformanceGoal(Base):

    __tablename__ = "performance_goals"

    goal_id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(Integer)

    target_score = Column(Integer)

    period = Column(
        String(20)
    )

    start_date = Column(DateTime)

    end_date = Column(DateTime)

    created_by = Column(Integer)