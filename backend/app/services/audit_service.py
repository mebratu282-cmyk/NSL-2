from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    user_id: int,
    action_type: str,
    details: str
):
    log = AuditLog(
        user_id=user_id,
        action_type=action_type,
        details=details
    )

    db.add(log)
    db.commit()