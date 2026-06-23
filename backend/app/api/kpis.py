from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.kpi import KPI
from app.models.employee_kpi import EmployeeKPI
from app.models.user import User

from app.schemas.kpi import (
    KPICreate,
    KPIAssignment
)

from app.core.roles import (
    require_admin,
    require_supervisor
)

from app.core.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/kpis",
    tags=["KPI Management"]
)


@router.post("/")
def create_kpi(

    kpi: KPICreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_admin
    )
):

    db_kpi = KPI(

        kpi_name=
            kpi.kpi_name,

        description=
            kpi.description,

        target_value=
            kpi.target_value
    )

    db.add(db_kpi)

    db.commit()

    db.refresh(db_kpi)

    return db_kpi

@router.get("/")
def get_kpis(
    db: Session = Depends(get_db)
):

    return (
        db.query(KPI)
        .all()
    )
    
@router.post("/assign")
def assign_kpi(

    assignment: KPIAssignment,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_admin
    )
):

    user = (
        db.query(User)
        .filter(
            User.user_id ==
            assignment.user_id
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    kpi = (
        db.query(KPI)
        .filter(
            KPI.kpi_id ==
            assignment.kpi_id
        )
        .first()
    )

    if not kpi:

        raise HTTPException(
            status_code=404,
            detail="KPI not found"
        )

    employee_kpi = EmployeeKPI(

        user_id=
            assignment.user_id,

        kpi_id=
            assignment.kpi_id
    )

    db.add(employee_kpi)

    db.commit()

    db.refresh(employee_kpi)

    return employee_kpi

@router.get("/my-kpis")
def my_kpis(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    results = (

        db.query(
            EmployeeKPI,
            KPI
        )

        .join(
            KPI,
            EmployeeKPI.kpi_id ==
            KPI.kpi_id
        )

        .filter(
            EmployeeKPI.user_id ==
            current_user.user_id
        )

        .all()
    )

    response = []

    for assignment, kpi in results:

        achievement = 0

        if kpi.target_value:

            achievement = round(
                (
                    assignment.current_value
                    /
                    kpi.target_value
                ) * 100,
                2
            )

        response.append({

            "employee_kpi_id":
                assignment.employee_kpi_id,

            "kpi_name":
                kpi.kpi_name,

            "target":
                kpi.target_value,

            "current":
                assignment.current_value,

            "achievement":
                achievement
        })

    return response

@router.get("/team")
def team_kpis(
    current_user=Depends(require_supervisor),
    db: Session = Depends(get_db)
):

    employees = (
        db.query(User)
        .filter(
            User.supervisor_id ==
            current_user.user_id
        )
        .all()
    )

    employee_ids = [
        emp.user_id
        for emp in employees
    ]

    return (
        db.query(EmployeeKPI)
        .filter(
            EmployeeKPI.user_id.in_(employee_ids)
        )
        .all()
    )