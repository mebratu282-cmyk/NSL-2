from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.user import User
from app.core.roles import require_admin

from app.schemas.user import UserCreate
from app.core.security import hash_password
from fastapi import HTTPException

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