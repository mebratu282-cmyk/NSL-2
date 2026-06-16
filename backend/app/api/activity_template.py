from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.activity_template import (
    ActivityTemplate
)

from app.schemas.activity_template import (
    ActivityTemplateCreate
)

router = APIRouter(
    prefix="/activity-templates",
    tags=["Activity Templates"]
)


@router.get("/")
def get_activity_templates(
    db: Session = Depends(get_db)
):
    return db.query(
        ActivityTemplate
    ).all()


@router.post("/")
def create_activity_template(
    activity: ActivityTemplateCreate,
    db: Session = Depends(get_db)
):
    db_activity = ActivityTemplate(
        service_id=activity.service_id,
        activity_name=activity.activity_name,
        standard_quantity=activity.standard_quantity,
        standard_duration_minutes=activity.standard_duration_minutes,
        standard_quality_percent=activity.standard_quality_percent
    )

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    return db_activity

@router.put("/{activity_id}")
def update_activity_template(
    activity_id: int,
    activity: ActivityTemplateCreate,
    db: Session = Depends(get_db)
):
    db_activity = db.query(
        ActivityTemplate
    ).filter(
        ActivityTemplate.activity_id == activity_id
    ).first()

    if not db_activity:
        return {
            "message": "Activity not found"
        }

    db_activity.service_id = activity.service_id
    db_activity.activity_name = activity.activity_name
    db_activity.standard_quantity = activity.standard_quantity
    db_activity.standard_duration_minutes = (
        activity.standard_duration_minutes
    )
    db_activity.standard_quality_percent = (
        activity.standard_quality_percent
    )

    db.commit()

    return {
        "message": "Activity updated"
    }

@router.delete("/{activity_id}")
def delete_activity_template(

    activity_id: int,
    db: Session = Depends(get_db)
):
    db_activity = db.query(
        ActivityTemplate
    ).filter(
        ActivityTemplate.activity_id == activity_id
    ).first()

    if not db_activity:
        return {
            "message": "Activity not found"
        }

    db.delete(db_activity)
    db.commit()

    return {
        "message": "Activity deleted"
    }

@router.get("/service/{service_id}")
def get_service_activities(
    service_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(ActivityTemplate)
        .filter(
            ActivityTemplate.service_id == service_id
        )
        .all()
    )