from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.department import Department
from app.schemas.department import (
    DepartmentCreate
)
from app.core.roles import require_admin


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post("/")
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):

    existing = (
        db.query(Department)
        .filter(
            Department.department_name
            == department.department_name
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )

    db_department = Department(
        department_name=department.department_name,
        description=department.description
    )

    db.add(db_department)
    db.commit()
    db.refresh(db_department)

    return db_department


@router.get("/")
def get_departments(
    db: Session = Depends(get_db)
):
    return db.query(Department).all()