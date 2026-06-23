from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.task_assignment import (
    TaskAssignment
)

from app.schemas.task import (
    TaskCreate,
    TaskStatusUpdate
)

from app.core.roles import (
    require_supervisor
)

from app.core.dependencies import (
    get_current_user
)
from app.services.notification_service import (
    create_notification
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)
@router.post("/")
def create_task(

    task: TaskCreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_supervisor
    )
):

    db_task = TaskAssignment(

        assigned_by=
            current_user.user_id,

        assigned_to=
            task.assigned_to,

        title=
            task.title,

        description=
            task.description,

        due_date=
            task.due_date
    )

    db.add(db_task)
    
    db.commit()
    create_notification(
        db=db,
        user_id=task.assigned_to,
        title="New Task Assigned",
        message=f"Task '{task.title}' assigned to you"
    )
    db.refresh(db_task)

    return db_task
   

    
@router.put("/{task_id}/status")
def update_task_status(

    task_id: int,

    request: TaskStatusUpdate,

    db: Session = Depends(get_db)
):

    task = (

        db.query(TaskAssignment)

        .filter(
            TaskAssignment.task_id
            == task_id
        )

        .first()
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.status = request.status

    db.commit()

    return {
        "message":
        "Task updated"
    }
    
@router.get("/assigned-by/{supervisor_id}")
def tasks_assigned_by(

    supervisor_id: int,

    db: Session = Depends(get_db)
):

    return (

        db.query(TaskAssignment)

        .filter(
            TaskAssignment.assigned_by
            == supervisor_id
        )

        .order_by(
            TaskAssignment.created_at.desc()
        )

        .all()
    )
    

    
@router.get("/my-tasks")
def my_tasks(
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return (
        db.query(TaskAssignment)
        .filter(
            TaskAssignment.assigned_to
            == current_user.user_id
        )
        .order_by(
            TaskAssignment.due_date
        )
        .all()
    )
    
@router.get("/my-assigned-tasks")
def my_assigned_tasks(
    current_user=Depends(
        require_supervisor
    ),
    db: Session = Depends(get_db)
):

    return (
        db.query(TaskAssignment)
        .filter(
            TaskAssignment.assigned_by
            == current_user.user_id
        )
        .order_by(
            TaskAssignment.created_at.desc()
        )
        .all()
    )
    
@router.put("/{task_id}/request-completion")
def request_completion(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(TaskAssignment)
        .filter(
            TaskAssignment.task_id == task_id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.status = "COMPLETION_REQUESTED"

    db.commit()
    create_notification(
        db=db,
        user_id=task.assigned_by,
        title="Task Completion Request",
        message=f"Employee requested completion of '{task.title}'"
    )
    return {
        "message":
        "Completion submitted"
    }
@router.put("/{task_id}/approve-completion")
def approve_completion(
    task_id: int,
    current_user=Depends(
        require_supervisor
    ),
    db: Session = Depends(get_db)
):

    task = (
        db.query(TaskAssignment)
        .filter(
            TaskAssignment.task_id == task_id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.status = "COMPLETED"

    db.commit()
    create_notification(
        db=db,
        user_id=task.assigned_to,
        title="Task Approved",
        message=f"Task '{task.title}' marked as completed"
    )
    return {
        "message":
        "Task approved"
    }
@router.get("/completion-requests")
def completion_requests(

    current_user=Depends(
        require_supervisor
    ),

    db: Session = Depends(get_db)
):

    return (

        db.query(TaskAssignment)

        .filter(
            TaskAssignment.assigned_by ==
            current_user.user_id,

            TaskAssignment.status ==
            "COMPLETION_REQUESTED"
        )

        .all()
    )
