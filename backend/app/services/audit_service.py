from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    user_id: int,
    action: str,
    details: str
):

    audit = AuditLog(
        user_id=user_id,
        action=action,
        details=details
    )

    db.add(audit)

    db.commit()