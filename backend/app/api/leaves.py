from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.leave_request import LeaveRequest
from app.models.user import User

from app.schemas.leave import (
    LeaveCreate,
    LeaveApproval
)

from app.core.dependencies import (
    get_current_user
)

from app.core.roles import (
    require_supervisor
)

from app.services.audit_service import (
    create_audit_log
)

from app.services.notification_service import (
    create_notification
)

router = APIRouter(
    prefix="/leaves",
    tags=["Leave Management"]
)

@router.post("/")
def create_leave(

    leave: LeaveCreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    db_leave = LeaveRequest(

        user_id=current_user.user_id,

        leave_type=leave.leave_type,

        start_date=leave.start_date,

        end_date=leave.end_date,

        reason=leave.reason
    )

    db.add(db_leave)

    db.commit()

    db.refresh(db_leave)

    employee = (
        db.query(User)
        .filter(
            User.user_id ==
            current_user.user_id
        )
        .first()
    )

    if employee and employee.supervisor_id:

        create_notification(
            db=db,
            user_id=employee.supervisor_id,
            title="Leave Request",
            message=f"{employee.full_name} submitted a leave request"
        )

    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action_type="CREATE_LEAVE",
        details=f"Created Leave Request #{db_leave.leave_id}"
    )

    return db_leave

@router.get("/my-leaves")
def my_leaves(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return (

        db.query(LeaveRequest)

        .filter(
            LeaveRequest.user_id ==
            current_user.user_id
        )

        .order_by(
            LeaveRequest.created_at.desc()
        )

        .all()
    )
@router.get("/pending")
def pending_leaves(

    current_user=Depends(
        require_supervisor
    ),

    db: Session = Depends(get_db)
):

    employees = (

        db.query(User)

        .filter(
            User.supervisor_id ==
            current_user.user_id
        )

        .all()
    )

    employee_ids = [
        employee.user_id
        for employee in employees
    ]

    return (

        db.query(LeaveRequest)

        .filter(
            LeaveRequest.user_id.in_(
                employee_ids
            ),

            LeaveRequest.status ==
            "PENDING"
        )

        .all()
    )
    
    

@router.put("/{leave_id}/approve")
def approve_leave(

    leave_id: int,

    request: LeaveApproval,

    current_user=Depends(
        require_supervisor
    ),

    db: Session = Depends(get_db)
):

    leave = (

        db.query(LeaveRequest)

        .filter(
            LeaveRequest.leave_id ==
            leave_id
        )

        .first()
    )

    if not leave:

        raise HTTPException(
            status_code=404,
            detail="Leave not found"
        )

    leave.status = "APPROVED"

    leave.approved_by = (
        current_user.user_id
    )

    leave.approval_comment = (
        request.approval_comment
    )

    db.commit()

    create_notification(
        db=db,
        user_id=leave.user_id,
        title="Leave Approved",
        message=f"Leave Request #{leave_id} approved"
    )

    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action_type="APPROVE_LEAVE",
        details=f"Approved Leave #{leave_id}"
    )

    return {
        "message": "Leave approved"
    }



@router.put("/{leave_id}/reject")
def reject_leave(

    leave_id: int,

    request: LeaveApproval,

    current_user=Depends(
        require_supervisor
    ),

    db: Session = Depends(get_db)
):

    leave = (

        db.query(LeaveRequest)

        .filter(
            LeaveRequest.leave_id ==
            leave_id
        )

        .first()
    )

    if not leave:

        raise HTTPException(
            status_code=404,
            detail="Leave not found"
        )

    leave.status = "REJECTED"

    leave.approved_by = (
        current_user.user_id
    )

    leave.approval_comment = (
        request.approval_comment
    )

    db.commit()

    create_notification(
        db=db,
        user_id=leave.user_id,
        title="Leave Rejected",
        message=f"Leave Request #{leave_id} rejected"
    )

    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action_type="REJECT_LEAVE",
        details=f"Rejected Leave #{leave_id}"
    )

    return {
        "message": "Leave rejected"
    }