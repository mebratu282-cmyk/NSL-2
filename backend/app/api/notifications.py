from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.notification import Notification
from app.services.notification_service import (
    create_notification
)
router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/{user_id}")
def get_notifications(
    user_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id
        )
        .order_by(
            Notification.created_at.desc()
        )
        .all()
    )
    
@router.post("/test/{user_id}")
def create_test_notification(
    user_id: int,
    db: Session = Depends(get_db)
):

    return create_notification(
        db=db,
        user_id=user_id,
        title="Test Notification",
        message="Notification system working"
    )