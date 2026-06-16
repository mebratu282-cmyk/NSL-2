from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.service import Service
from app.schemas.service import ServiceCreate

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


@router.get("/")
def get_services(
    db: Session = Depends(get_db)
):
    return db.query(Service).all()


@router.post("/")
def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db)
):
    db_service = Service(
        category_id=service.category_id,
        service_name=service.service_name
    )

    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    return db_service