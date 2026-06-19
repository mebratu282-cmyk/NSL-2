from app.database.connection import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

user = (
    db.query(User)
    .filter(
        User.employee_code == "ADMIN001"
    )
    .first()
)

user.password_hash = hash_password(
    "admin1234"
)

db.commit()

print("Password reset complete")