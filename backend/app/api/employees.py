from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.employee import Employee
from app.models.department import Department

from app.schemas.employee import (
EmployeeCreate,
EmployeeUpdate
)
from app.services.audit_service import (
    create_audit_log
)

from app.core.roles import require_admin

router = APIRouter(
prefix="/employees",
tags=["Employees"]
)

@router.post("/")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
    ):


    department = (
        db.query(Department)
        .filter(
            Department.department_id
            ==
            employee.department_id
        )
        .first()
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    existing_employee = (
        db.query(Employee)
        .filter(
            Employee.employee_code
            ==
            employee.employee_code
        )
        .first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Employee code already exists"
        )

    db_employee = Employee(
        employee_code=
            employee.employee_code,

        full_name=
            employee.full_name,

        phone=
            employee.phone,

        email=
            employee.email,

        department_id=
            employee.department_id
    )

   
    
   
    
    db.add(employee)

    db.commit()

    db.refresh(employee)
    return db_employee

    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action_type="CREATE_EMPLOYEE",
        details=f"Created Employee {employee.employee_code}"
    )
@router.get("/")
def get_employees(
    db: Session = Depends(get_db)
    ):
    return db.query(Employee).all()

@router.get("/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
    ):


    employee = (
        db.query(Employee)
        .filter(
            Employee.employee_id
            ==
            employee_id
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


@router.put("/{employee_id}")
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
    ):


    employee = (
        db.query(Employee)
        .filter(
            Employee.employee_id
            ==
            employee_id
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    setattr(
        employee,
        "employee_code",
        employee_data.employee_code
    )

    setattr(
        employee,
        "full_name",
        employee_data.full_name
    )

    setattr(
        employee,
        "phone",
        employee_data.phone
    )

    setattr(
        employee,
        "email",
        employee_data.email
    )

    setattr(
        employee,
        "department_id",
        employee_data.department_id
    )
    db.commit()

    db.refresh(employee)

    return {
        "message":
        "Employee updated"
    }


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
    ):

    employee = (
        db.query(Employee)
        .filter(
            Employee.employee_id
            ==
            employee_id
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)

    db.commit()

    return {
        "message":
        "Employee deleted"
    }

