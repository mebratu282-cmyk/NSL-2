from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.audit_log import AuditLog

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)

@router.get("/")
def get_audit_logs(
    db: Session = Depends(get_db)
):
    return (
        db.query(AuditLog)
        .order_by(
            AuditLog.action_date.desc()
        )
        .all()
    )