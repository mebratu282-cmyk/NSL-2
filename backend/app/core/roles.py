from fastapi import Depends
from fastapi import HTTPException

from app.core.dependencies import get_current_user


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user
def require_supervisor(
    current_user=Depends(get_current_user)
):
    if current_user.role not in [
        "SUPERVISOR",
        "ADMIN"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Supervisor access required"
        )

    return current_user