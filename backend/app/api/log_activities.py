from tempfile import template

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.log_activity import LogActivity

from app.schemas.log_activity import (
    LogActivityCreate
)
from app.models.activity_template import (
    ActivityTemplate
)

from app.models.performance_result import (
    PerformanceResult
)

from app.services.performance_calculator import (
    calculate_scores
)

router = APIRouter(
    prefix="/log-activities",
    tags=["Log Activities"]
)


@router.post("/")
def create_log_activity(
    activity: LogActivityCreate,
    db: Session = Depends(get_db)
):

    db_activity = LogActivity(
        log_id=activity.log_id,
        activity_id=activity.activity_id,
        quantity_completed=
            activity.quantity_completed,
        duration_minutes=
            activity.duration_minutes,
        quality_percent=
            activity.quality_percent
    )

    db.add(db_activity)

    db.commit()

    db.refresh(db_activity)
    
    template = (
        db.query(ActivityTemplate)
        .filter(
            ActivityTemplate.activity_id == db_activity.activity_id
        )
        .first()
    )

    if template:

        scores = calculate_scores(
            quantity_completed=
                db_activity.quantity_completed,

            duration_minutes=
                db_activity.duration_minutes,

            quality_percent=
                db_activity.quality_percent,

            standard_quantity=
                template.standard_quantity,

            standard_duration=
                template.standard_duration_minutes,

            standard_quality=
                template.standard_quality_percent
        )

        result = PerformanceResult(
            log_activity_id=
                db_activity.log_activity_id,

            quantity_score=
                scores["quantity_score"],

            time_score=
                scores["time_score"],

            quality_score=
                scores["quality_score"],

            final_score=
                scores["final_score"]
        )

        db.add(result)

        db.commit()
    return db_activity

@router.get("/")
def get_log_activities(
    db: Session = Depends(get_db)
):
    return db.query(
        LogActivity
    ).all()


@router.get("/log/{log_id}")
def get_log_activity_by_log(
    log_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(LogActivity)
        .filter(
            LogActivity.log_id == log_id
        )
        .all()
    )