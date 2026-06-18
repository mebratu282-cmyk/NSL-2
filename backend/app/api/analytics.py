from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db

from app.models.performance_result import (
PerformanceResult
)
from app.models.user import User
from app.models.daily_log import DailyLog
from app.models.log_activity import LogActivity






router = APIRouter(
prefix="/analytics",
tags=["Analytics"]
)

@router.get("/overview")
def analytics_overview(
    db: Session = Depends(get_db)
    ):

    result = (
        db.query(
            func.count(
                PerformanceResult.result_id
            ),
            func.avg(
                PerformanceResult.final_score
            ),
            func.max(
                PerformanceResult.final_score
            ),
            func.min(
                PerformanceResult.final_score
            )
        )
        .first()
    )

    return {
        "total_records":
            result[0] or 0,

        "average_score":
            round(float(result[1] or 0), 2),

        "highest_score":
            round(float(result[2] or 0), 2),

        "lowest_score":
            round(float(result[3] or 0), 2)
    }

@router.get("/top-performers")
def top_performers(
    db: Session = Depends(get_db)
    ):

    results = (
        db.query(
            User.user_id,
            User.employee_code,
            User.full_name,
            func.avg(
                PerformanceResult.final_score
            ).label("avg_score")
        )
        .join(
            DailyLog,
            DailyLog.user_id == User.user_id
        )
        .join(
            LogActivity,
            LogActivity.log_id == DailyLog.log_id
        )
        .join(
            PerformanceResult,
            PerformanceResult.log_activity_id
            ==
            LogActivity.log_activity_id
        )
        .group_by(
            User.user_id,
            User.employee_code,
            User.full_name
        )
        .order_by(
            func.avg(
                PerformanceResult.final_score
            ).desc()
        )
        .limit(5)
        .all()
    )

    return [
        {
            "user_id": row[0],
            "employee_code": row[1],
            "full_name": row[2],
            "average_score": round(float(row[3]), 2)
        }
        for row in results
    ]
    
@router.get("/score-trend")
def score_trend(
    db: Session = Depends(get_db)
    ):


    results = (
        db.query(
            PerformanceResult.calculated_at,
            func.avg(
                PerformanceResult.final_score
            )
        )
        .group_by(
            PerformanceResult.calculated_at
        )
        .order_by(
            PerformanceResult.calculated_at
        )
        .all()
    )

    return [
        {
            "date":
                str(row[0]),

            "average_score":
                round(float(row[1]), 2)
        }
        for row in results
    ]
@router.get("/department-performance")
def department_performance(
    db: Session = Depends(get_db)
    ):

    results = (
        db.query(
            User.department,
            func.count(
                func.distinct(User.user_id)
            ),
            func.avg(
                PerformanceResult.final_score
            )
        )
        .join(
            DailyLog,
            DailyLog.user_id == User.user_id
        )
        .join(
            LogActivity,
            LogActivity.log_id == DailyLog.log_id
        )
        .join(
            PerformanceResult,
            PerformanceResult.log_activity_id
            ==
            LogActivity.log_activity_id
        )
        .group_by(
            User.department
        )
        .all()
    )

    return [
        {
            "department": row[0],
            "employee_count": row[1],
            "average_score":
                round(float(row[2]), 2)
        }
        for row in results
    ]
    
    

