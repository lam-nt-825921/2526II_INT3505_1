from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 2. Tạo nhà máy sản xuất Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Tạo một cái Base class. Lát nữa file Models sẽ kế thừa cái này
Base = declarative_base()
