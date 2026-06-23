from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User

router = APIRouter(
    prefix="/team",
    tags=["Team"]
)

@router.get("/{supervisor_id}")
def get_my_team(
    supervisor_id: int,
    db: Session = Depends(get_db)
):

    employees = (
        db.query(User)
        .filter(
            User.supervisor_id == supervisor_id
        )
        .all()
    )

    return employees