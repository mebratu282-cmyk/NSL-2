from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.service_category import ServiceCategory
from app.schemas.service_category import ServiceCategoryCreate

router = APIRouter(
    prefix="/service-categories",
    tags=["Service Categories"]
)


@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(ServiceCategory).all()


@router.post("/")
def create_category(
    category: ServiceCategoryCreate,
    db: Session = Depends(get_db)
):
    db_category = ServiceCategory(
        category_name=category.category_name
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category

