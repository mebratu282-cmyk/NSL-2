from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.daily_log_activity import (
    DailyLogActivity
)

from app.schemas.daily_log_activity import (
    DailyLogActivityCreate
)

router = APIRouter(
    prefix="/daily-log-activities",
    tags=["Daily Log Activities"]
)

@router.get("/")
def get_daily_log_activities(
    db: Session = Depends(get_db)
):
    return db.query(
        DailyLogActivity
    ).all()

@router.post("/")
def create_daily_log_activity(
    activity: DailyLogActivityCreate,
    db: Session = Depends(get_db)
):
    db_activity = DailyLogActivity(
        log_id=activity.log_id,
        activity_id=activity.activity_id,
        actual_quantity=activity.actual_quantity,
        start_time=activity.start_time,
        end_time=activity.end_time,
        duration_minutes=activity.duration_minutes,
        quality_percent=activity.quality_percent,
        remarks=activity.remarks
    )

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    return db_activity
@router.delete("/{activity_log_id}")
def delete_daily_log_activity(
    activity_log_id: int,
    db: Session = Depends(get_db)
):
    activity = db.query(
        DailyLogActivity
    ).filter(
        DailyLogActivity.activity_log_id
        == activity_log_id
    ).first()

    if not activity:
        return {
            "message": "Not found"
        }

    db.delete(activity)
    db.commit()

    return {
        "message": "Deleted"
    }