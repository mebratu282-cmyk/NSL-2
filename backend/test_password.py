from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

hash_from_db = "$2b$12$/CyUyJIgRW0nI5.nsCgfD.lSxaOsDYSHleYlrP63.6tly8EVDR05O"

print(
    pwd_context.verify(
        "admin123",
        hash_from_db
    )
)