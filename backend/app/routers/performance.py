from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db

from app.models.user import User
from app.models.daily_log import DailyLog
from app.models.log_activity import LogActivity
from app.models.performance_result import (
    PerformanceResult
)

router = APIRouter(
    prefix="/performance",
    tags=["Performance"]
)


@router.get("/my-performance/{user_id}")
def my_performance(
    user_id: int,
    db: Session = Depends(get_db)
):

    total_logs = (
        db.query(DailyLog)
        .filter(
            DailyLog.user_id == user_id
        )
        .count()
    )

    avg_score = (
        db.query(
            func.avg(
                PerformanceResult.final_score
            )
        )
        .join(
            LogActivity,
            LogActivity.log_activity_id ==
            PerformanceResult.log_activity_id
        )
        .join(
            DailyLog,
            DailyLog.log_id ==
            LogActivity.log_id
        )
        .filter(
            DailyLog.user_id == user_id
        )
        .scalar()
    )

    best_score = (
        db.query(
            func.max(
                PerformanceResult.final_score
            )
        )
        .join(
            LogActivity,
            LogActivity.log_activity_id ==
            PerformanceResult.log_activity_id
        )
        .join(
            DailyLog,
            DailyLog.log_id ==
            LogActivity.log_id
        )
        .filter(
            DailyLog.user_id == user_id
        )
        .scalar()
    )

    return {
        "total_logs": total_logs,
        "average_score":
            round(float(avg_score or 0), 2),
        "best_score":
            round(float(best_score or 0), 2)
    }