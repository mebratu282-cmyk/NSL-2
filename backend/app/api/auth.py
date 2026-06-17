from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import String
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.core.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm 
from app.core.security import (
    verify_password,
    create_access_token
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

password_hash: Mapped[str] = mapped_column(
    String(255)
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.employee_code == form_data.username

        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {
            "sub": user.employee_code,
            "role": user.role,
            "user_id": user.user_id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "employee_code": current_user.employee_code,
        "full_name": current_user.full_name,
        "role": current_user.role
    }