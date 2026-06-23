from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.daily_log import DailyLog
from app.schemas.daily_log import DailyLogCreate
from app.schemas.approval import ApprovalRequest
from app.core.roles import require_admin,require_supervisor
from app.models.user import User
from app.services.audit_service import create_audit_log
from app.services.audit_service import (
    create_audit_log
)
from app.services.notification_service import (
    create_notification
    )
from app.models.service import Service
from app.schemas.supervisor import (
    PendingLogResponse
)


router = APIRouter(
    prefix="/daily-logs",
    tags=["Daily Logs"]
)

@router.post("/")
def create_log(
    log: DailyLogCreate,
    db: Session = Depends(get_db)
):

    db_log = DailyLog(
        user_id=log.user_id,
        service_id=log.service_id,
        log_date=log.log_date,
        status="DRAFT"
    )

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return {
        "log_id": db_log.log_id
    }

@router.get("/")
def get_logs(

    db: Session = Depends(get_db)
):
    return db.query(DailyLog).all()

@router.put("/{log_id}/approve")
def approve_log(
    log_id: int,
    request: ApprovalRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor)
):

    log = (
        db.query(DailyLog)
        .filter(
            DailyLog.log_id == log_id
        )
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    log.status = "APPROVED"

    log.approved_by = current_user.user_id

    log.approval_comment = request.approval_comment

    db.commit()
    create_notification(
        db=db,
        user_id=log.user_id,
        title="Log Approved",
        message=f"Daily Log #{log_id} was approved"
        )
    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action_type="APPROVE_LOG",
        details=f"Approved Daily Log #{log_id}"
    )
    return {
        "message": "Log approved"
    }
    
    

@router.put("/{log_id}/reject")
def reject_log(
    log_id: int,
    request: ApprovalRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor)
):

    log = (
        db.query(DailyLog)
        .filter(
            DailyLog.log_id == log_id
        )
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    log.status = "REJECTED"

    log.approved_by = current_user.user_id

    log.approval_comment = request.approval_comment

    db.commit()
    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action_type="REJECT_LOG",
        details=f"Rejected Daily Log #{log_id}"
    )
    create_notification(
        db=db,
        user_id=log.user_id,
        title="Log Rejected",
        message=f"Daily Log #{log_id} was rejected"
    )
    return {
        "message": "Log rejected"
    }
    


@router.put("/{log_id}/submit")
def submit_log(
    log_id: int,
    db: Session = Depends(get_db)
):

    log = (
        db.query(DailyLog)
        .filter(
            DailyLog.log_id == log_id
        )
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    log.status = "SUBMITTED"

    db.commit()

    employee = (
        db.query(User)
        .filter(
            User.user_id == log.user_id
        )
        .first()
    )

    if employee and employee.supervisor_id:

        create_notification(
            db=db,
            user_id=employee.supervisor_id,
            title="New Submission",
            message=f"Daily Log #{log_id} awaiting review"
        )

    create_audit_log(
        db=db,
        user_id=log.user_id,
        action_type="SUBMIT_LOG",
        details=f"Submitted Daily Log #{log_id}"
    )

    return {
        "message": "Log submitted"
    }
 
    
@router.get("/pending/{supervisor_id}")
def get_pending_logs(
    supervisor_id: int,
    db: Session = Depends(get_db)
):

    employee_ids = [
        user.user_id
        for user in db.query(User)
        .filter(
            User.supervisor_id == supervisor_id
        )
        .all()
    ]

    logs = (
        db.query(DailyLog)
        .filter(
            DailyLog.user_id.in_(employee_ids),
            DailyLog.status == "SUBMITTED"
        )
        .all()
    )

    return logs

@router.get(
    "/pending-details/{supervisor_id}",
    response_model=list[PendingLogResponse]
)
def get_pending_logs_details(
    supervisor_id: int,
    db: Session = Depends(get_db)
):
    logs = (
        db.query(
            DailyLog.log_id,
            User.full_name.label(
                "employee_name"
            ),
            Service.service_name.label(
                "service_name"
            ),
            DailyLog.log_date,
            DailyLog.status
        )
        .join(
            User,
            DailyLog.user_id ==
            User.user_id
        )
        .join(
            Service,
            DailyLog.service_id ==
            Service.service_id
        )
        .filter(
            DailyLog.status ==
            "SUBMITTED"
        )
        .all()
    )

    return logs

