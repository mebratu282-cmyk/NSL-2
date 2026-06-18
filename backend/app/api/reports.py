from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db

from app.models.user import User
from app.models.daily_log import DailyLog
from app.models.log_activity import LogActivity
from app.models.performance_result import (
PerformanceResult
)
from fastapi.responses import FileResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

import tempfile
from openpyxl import Workbook
from fastapi.responses import FileResponse
import tempfile
router = APIRouter(
prefix="/reports",
tags=["Reports"]
)

@router.get("/employee/{user_id}")
def employee_report(
    user_id: int,
    db: Session = Depends(get_db)
    ):

    employee = (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    report = (
        db.query(
            func.count(
                PerformanceResult.result_id
            ),
            func.avg(
                PerformanceResult.final_score
            ),
            func.max(
                PerformanceResult.final_score
            ),
            func.min(
                PerformanceResult.final_score
            )
        )
        .join(
            LogActivity,
            PerformanceResult.log_activity_id
            ==
            LogActivity.log_activity_id
        )
        .join(
            DailyLog,
            LogActivity.log_id
            ==
            DailyLog.log_id
        )
        .filter(
            DailyLog.user_id == user_id
        )
        .first()
    )

    return {
        "employee_name":
            employee.full_name,

        "total_activities":
            report[0] or 0,

        "average_score":
            round(float(report[1] or 0), 2),

        "best_score":
            round(float(report[2] or 0), 2),

        "lowest_score":
            round(float(report[3] or 0), 2)
    }

@router.get("/employee/{user_id}/pdf")
def employee_report_pdf(
    user_id: int,
    db: Session = Depends(get_db)
    ):

    employee = (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )

    report = (
        db.query(
            func.count(
                PerformanceResult.result_id
            ),
            func.avg(
                PerformanceResult.final_score
            ),
            func.max(
                PerformanceResult.final_score
            ),
            func.min(
                PerformanceResult.final_score
            )
        )
        .join(
            LogActivity,
            PerformanceResult.log_activity_id
            ==
            LogActivity.log_activity_id
        )
        .join(
            DailyLog,
            LogActivity.log_id
            ==
            DailyLog.log_id
        )
        .filter(
            DailyLog.user_id == user_id
        )
        .first()
    )

    pdf_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    doc = SimpleDocTemplate(
        pdf_file.name
    )

    styles = getSampleStyleSheet()

    content = [

        Paragraph(
            "Employee Performance Report",
            styles["Title"]
        ),

        Spacer(1, 20),

        Paragraph(
            f"Employee: {employee.full_name}",
            styles["Normal"]
        ),

        Paragraph(
            f"Total Activities: {report[0] or 0}",
            styles["Normal"]
        ),

        Paragraph(
            f"Average Score: {round(float(report[1] or 0), 2)}",
            styles["Normal"]
        ),

        Paragraph(
            f"Best Score: {round(float(report[2] or 0), 2)}",
            styles["Normal"]
        ),

        Paragraph(
            f"Lowest Score: {round(float(report[3] or 0), 2)}",
            styles["Normal"]
        )

    ]

    doc.build(content)

    return FileResponse(
        pdf_file.name,
        filename="employee_report.pdf",
        media_type="application/pdf"
    )

@router.get("/employee/{user_id}/excel")
def employee_report_excel(
    user_id: int,
    db: Session = Depends(get_db)
    ):

    employee = (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )

    report = (
        db.query(
            func.count(
                PerformanceResult.result_id
            ),
            func.avg(
                PerformanceResult.final_score
            ),
            func.max(
                PerformanceResult.final_score
            ),
            func.min(
                PerformanceResult.final_score
            )
        )
        .join(
            LogActivity,
            PerformanceResult.log_activity_id
            ==
            LogActivity.log_activity_id
        )
        .join(
            DailyLog,
            LogActivity.log_id
            ==
            DailyLog.log_id
        )
        .filter(
            DailyLog.user_id == user_id
        )
        .first()
    )

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Performance Report"

    sheet.append(
        ["Employee", employee.full_name]
    )

    sheet.append(
        ["Total Activities", report[0] or 0]
    )

    sheet.append(
        ["Average Score",
        round(float(report[1] or 0), 2)]
    )

    sheet.append(
        ["Best Score",
        round(float(report[2] or 0), 2)]
    )

    sheet.append(
        ["Lowest Score",
        round(float(report[3] or 0), 2)]
    )

    file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".xlsx"
    )

    workbook.save(file.name)

    return FileResponse(
        file.name,
        filename="employee_report.xlsx",
        media_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
