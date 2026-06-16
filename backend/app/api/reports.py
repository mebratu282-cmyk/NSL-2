from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db

from app.models.user import User
from app.models.daily_log import DailyLog
from app.models.performance_result import (
    PerformanceResult
)
from app.models.log_activity import LogActivity

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get("/employee-history/{user_id}")
def employee_history(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if not user:
        return {
            "message": "User not found"
        }

    logs = (
        db.query(DailyLog)
        .filter(
            DailyLog.user_id == user_id
        )
        .all()
    )

    return {
        "employee_code": user.employee_code,
        "full_name": user.full_name,
        "logs": logs
    }

@router.get("/monthly-performance")
def monthly_performance(
    db: Session = Depends(get_db)
):

    avg_score = (
        db.query(
            func.avg(
                PerformanceResult.final_score
            )
        )
        .scalar()
    )

    total_logs = (
        db.query(DailyLog)
        .count()
    )

    approved_logs = (
        db.query(DailyLog)
        .filter(
            DailyLog.status == "APPROVED"
        )
        .count()
    )

    submitted_logs = (
        db.query(DailyLog)
        .filter(
            DailyLog.status == "SUBMITTED"
        )
        .count()
    )

    return {
        "total_logs": total_logs,
        "approved_logs": approved_logs,
        "submitted_logs": submitted_logs,
        "average_score": round(
            float(avg_score or 0),
            2
        )
    }