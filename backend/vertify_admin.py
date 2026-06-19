from app.database.connection import SessionLocal
from app.models.user import User
from app.core.security import verify_password

db = SessionLocal()

user = (
    db.query(User)
    .filter(
        User.employee_code == "ADMIN001"
    )
    .first()
)

print("Hash:", user.password_hash)

print(
    "Match:",
    verify_password(
        "admin1234",
        user.password_hash
    )
)