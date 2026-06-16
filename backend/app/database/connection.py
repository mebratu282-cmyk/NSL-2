from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = "system"
DB_PASSWORD = "p1rphwgbm"
DB_HOST = "localhost"
DB_PORT = "1521"
DB_SERVICE_NAME = "XEPDB1"

DATABASE_URL = (
    f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()