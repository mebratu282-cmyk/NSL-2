from app.core.security import hash_password
from app.core.security import verify_password

pwd = "123"

hashed = hash_password(pwd)

print(hashed)

print(
    verify_password(
        "123",
        hashed
    )
)