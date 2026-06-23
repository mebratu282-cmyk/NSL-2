from fastapi import FastAPI
from app.api.users import router as users_router
from app.database.base import Base
from app.api.performance import router as performance_router
from app.database.connection import engine
from app.api.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.models.user import User
from app.models.department import Department
from app.models.employee import Employee
from app.models.daily_log import DailyLog
from app.api.departments import router as departments_router
from app.models.approval import Approval
from app.api.audit import router as audit_router
from app.api.audit_logs import (
    router as audit_logs_router
)
from app.api.service_categories import (
    router as service_categories_router
)
from app.api import analytics

from app.models.log_activity import (
    LogActivity
)
from app.api.log_activities import (
    router as log_activities_router
)
from app.api.services import (
    router as services_router
)
from app.api.dashboard import (
    router as dashboard_router
)
from app.api.employees import (
    router as employees_router
)
from app.api.daily_logs import (
    router as daily_logs_router
)
from app.api.log_activities import (
    router as log_activities_router
)
from app.models.performance_result import (
    PerformanceResult
)
from app.api.performance import (
    router as performance_router
)
from app.api.reports import (
    router as reports_router
)
from app.models.service_category import ServiceCategory
from app.models.service import Service
from app.api.leaves import router as leaves_router
from app.api.activity_template import (
    router as activity_template_router
)
from app.models.daily_log_activity import (
    DailyLogActivity
)
from app.api.team import (
    router as team_router
)
from app.api.daily_log_activities import (
    router as daily_log_activities_router
)
from app.api.audit_logs import (
    router as audit_logs_router
)
from app.api.notifications import (
    router as notifications_router
)
from app.api.tasks import (
    router as tasks_router
)
app = FastAPI(
    title="NSL Government Service System",
    version="1.0.0"
)
app.include_router(departments_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(employees_router)
app.include_router(daily_logs_router)
app.include_router(dashboard_router)
app.include_router(service_categories_router)
app.include_router(services_router)
app.include_router(activity_template_router)
app.include_router(daily_log_activities_router)
app.include_router(log_activities_router)
app.include_router(reports_router)
app.include_router(team_router)
app.include_router(
    audit_logs_router
)
app.include_router(
    tasks_router
)
app.include_router(
    log_activities_router
)
app.include_router(
analytics.router
)
app.include_router(
    performance_router
)
app.include_router(
    audit_router
)
app.include_router(
    notifications_router
)
app.include_router(leaves_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "NSL API running"
    }

@app.get("/oracle-test")
def oracle_test():
    return {"status": "oracle connected"}