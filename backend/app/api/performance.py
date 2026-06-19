from decimal import Decimal

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.log_activity import LogActivity
from app.models.activity_template import ActivityTemplate
from app.models.performance_result import PerformanceResult

from sqlalchemy import func, desc
from app.models.user import User
from app.models.daily_log import DailyLog
from app.models.log_activity import LogActivity
from app.models.performance_result import PerformanceResult




from app.services.performance_calculator import (
    calculate_scores
)

router = APIRouter(
    prefix="/performance",
    tags=["Performance"]
)


@router.post("/calculate/{log_activity_id}")
def calculate_performance(
    log_activity_id: int,
    db: Session = Depends(get_db)
):

    log_activity = (
        db.query(LogActivity)
        .filter(
            LogActivity.log_activity_id ==
            log_activity_id
        )
        .first()
    )

    if not log_activity:
        raise HTTPException(
            status_code=404,
            detail="Log activity not found"
        )

    activity_template = (
        db.query(ActivityTemplate)
        .filter(
            ActivityTemplate.activity_id ==
            log_activity.activity_id
        )
        .first()
    )

    if not activity_template:
        raise HTTPException(
            status_code=404,
            detail="Activity template not found"
        )

    scores = calculate_scores(
        quantity_completed=
            log_activity.quantity_completed,

        duration_minutes=
            log_activity.duration_minutes,

        quality_percent=
            float(
                log_activity.quality_percent  # type: ignore[arg-type]
            ),

        standard_quantity=
            activity_template.standard_quantity,

        standard_duration=
            activity_template.standard_duration_minutes,

        standard_quality=
            activity_template.standard_quality_percent
    )

    result = PerformanceResult(
        log_activity_id=log_activity_id,
        quantity_score=scores[
            "quantity_score"
        ],
        time_score=scores[
            "time_score"
        ],
        quality_score=scores[
            "quality_score"
        ],
        final_score=scores[
            "final_score"
        ]
    )

    db.add(result)

    db.commit()

    db.refresh(result)

    return result

@router.get("/user/{user_id}")
def employee_performance_summary(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    total_activities = (
        db.query(LogActivity)
        .join(
            DailyLog,
            LogActivity.log_id == DailyLog.log_id
        )
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
            PerformanceResult.log_activity_id ==
            LogActivity.log_activity_id
        )
        .join(
            DailyLog,
            LogActivity.log_id ==
            DailyLog.log_id
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
            PerformanceResult.log_activity_id ==
            LogActivity.log_activity_id
        )
        .join(
            DailyLog,
            LogActivity.log_id ==
            DailyLog.log_id
        )
        .filter(
            DailyLog.user_id == user_id
        )
        .scalar()
    )

    lowest_score = (
        db.query(
            func.min(
                PerformanceResult.final_score
            )
        )
        .join(
            LogActivity,
            PerformanceResult.log_activity_id ==
            LogActivity.log_activity_id
        )
        .join(
            DailyLog,
            LogActivity.log_id ==
            DailyLog.log_id
        )
        .filter(
            DailyLog.user_id == user_id
        )
        .scalar()
    )

    return {
        "user_id": user.user_id,
        "employee_code": user.employee_code,
        "full_name": user.full_name,
        "total_activities": total_activities,
        "average_score": round(float(avg_score or 0), 2),
        "best_score": round(float(best_score or 0), 2),
        "lowest_score": round(float(lowest_score or 0), 2)
    }

@router.get("/leaderboard")
def performance_leaderboard(
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
            == LogActivity.log_activity_id
        )
        .group_by(
            User.user_id,
            User.employee_code,
            User.full_name
        )
        .order_by(
            desc("avg_score")
        )
        .all()
    )

    leaderboard = []

    rank = 1

    for row in results:

        leaderboard.append(
            {
                "rank": rank,
                "user_id": row.user_id,
                "employee_code": row.employee_code,
                "full_name": row.full_name,
                "average_score": round(
                    float(row.avg_score),
                    2
                )
            }
        )

        rank += 1

    return leaderboard

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