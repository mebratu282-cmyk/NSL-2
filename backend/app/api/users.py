from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.audit_service import (
    create_audit_log
)
from app.models.user import User
from app.core.roles import require_admin

from app.schemas.user import UserCreate
from app.core.security import hash_password
from fastapi import HTTPException
from fastapi import Depends
from app.core.dependencies import get_current_user
from app.core.security import (
    verify_password,
    hash_password
)
from app.schemas.change_password import (
    ChangePasswordRequest
)
from app.schemas.user import(
    SupervisorAssignment
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()


@router.post("/")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    db_user = User(
        username=user.username,
        full_name=user.full_name,
        password_hash=hash_password(user.password),
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "User created successfully"
    }
@router.get("/admin-only")
def admin_only(
    current_user=Depends(require_admin)
):
    return {
        "message": "Welcome Admin"
    }
    
@router.get("/me")
def get_my_profile(
    current_user=Depends(
    get_current_user
    )
    ):

    return {
        "user_id":
            current_user.user_id,

        "employee_code":
            current_user.employee_code,

        "full_name":
            current_user.full_name,

        "role":
            current_user.role,

        "department":
            current_user.department,

        "phone":
            current_user.phone,

        "last_login":
            current_user.last_login
    }
@router.put("/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(
        request.current_password,
        str(current_user.password_hash)
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password incorrect"
        )

    current_user.password_hash = hash_password(
        request.new_password
    )

    db.commit()
   
    return {
        "message": "Password updated"
    }
    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action_type="CHANGE_PASSWORD",
        details="User changed password"
    )
    
@router.put("/{user_id}/assign-supervisor")
def assign_supervisor(
    user_id: int,
    assignment: SupervisorAssignment,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    print("USER ID:", user_id)
    print("SUPERVISOR ID:", assignment.supervisor_id)

    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    supervisor = (
        db.query(User)
        .filter(
            User.user_id == assignment.supervisor_id
        )
        .first()
    )

    if not supervisor:
        raise HTTPException(
            status_code=404,
            detail="Supervisor not found"
        )

    if supervisor.role != "SUPERVISOR":
        raise HTTPException(
            status_code=400,
            detail="Selected user is not a supervisor"
        )

    user.supervisor_id = assignment.supervisor_id

    db.commit()

    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action_type="ASSIGN_SUPERVISOR",
        details=f"Assigned {user.employee_code} to {supervisor.employee_code}"
    )

    return {
        "message": "Supervisor assigned"
    }  
@router.get("/test-supervisor/{user_id}")
def test_supervisor(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    return user