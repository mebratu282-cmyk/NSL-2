from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.department import Department
from app.models.employee import Employee
from app.models.daily_log import DailyLog
from sqlalchemy import func

from app.models.user import User
from app.models.daily_log import DailyLog
from app.models.log_activity import LogActivity
from app.models.performance_result import (
    PerformanceResult
)
from app.models.user import User
from app.models.daily_log import DailyLog
from app.models.approval import Approval

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db)
):

    return {
        "departments":
            db.query(Department).count(),

        "employees":
            db.query(Employee).count(),

        "daily_logs":
            db.query(DailyLog).count(),

        "pending_logs":
            db.query(DailyLog)
            .filter(
                DailyLog.status == "PENDING"
            )
            .count()
    }
@router.get("/supervisor/{supervisor_id}")
def supervisor_dashboard(
    supervisor_id: int,
    db: Session = Depends(get_db)
):

    employee_ids = [
        u.user_id
        for u in db.query(User)
        .filter(
            User.supervisor_id == supervisor_id
        )
        .all()
    ]

    pending_logs = (
        db.query(DailyLog)
        .filter(
            DailyLog.user_id.in_(employee_ids),
            DailyLog.status == "SUBMITTED"
        )
        .count()
    )

    approved_logs = (
        db.query(Approval)
        .filter(
            Approval.approved_by == supervisor_id,
            Approval.approval_status == "APPROVED"
        )
        .count()
    )

    rejected_logs = (
        db.query(Approval)
        .filter(
            Approval.approved_by == supervisor_id,
            Approval.approval_status == "REJECTED"
        )
        .count()
    )

    return {
        "pending_logs": pending_logs,
        "approved_logs": approved_logs,
        "rejected_logs": rejected_logs
    }

@router.get("/overview")
def dashboard_overview(
    db: Session = Depends(get_db)
):

    total_employees = (
        db.query(User)
        .filter(
            User.role == "EMPLOYEE"
        )
        .count()
    )

    pending_logs = (
        db.query(DailyLog)
        .filter(
            DailyLog.status == "SUBMITTED"
        )
        .count()
    )

    approved_logs = (
        db.query(DailyLog)
        .filter(
            DailyLog.status == "APPROVED"
        )
        .count()
    )

    avg_score = (
        db.query(
            func.avg(
                PerformanceResult.final_score
            )
        )
        .scalar()
    )

    top_performer = (
        db.query(
            User.full_name,
            func.avg(
                PerformanceResult.final_score
            ).label("score")
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
            User.full_name
        )
        .order_by(
            func.avg(
                PerformanceResult.final_score
            ).desc()
        )
        .first()
    )

    return {
        "total_employees": total_employees,
        "pending_logs": pending_logs,
        "approved_logs": approved_logs,
        "average_score": round(
            float(avg_score or 0),
            2
        ),
        "top_performer":
            top_performer.full_name
            if top_performer
            else None
    }