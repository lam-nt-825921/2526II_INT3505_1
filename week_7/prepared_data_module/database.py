from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_demo.db"

# Khởi tạo engine kết nối SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Khởi tạo phiên làm việc (Session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho các DB Model
Base = declarative_base()

# Dependency dùng trong FastAPI Router
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
