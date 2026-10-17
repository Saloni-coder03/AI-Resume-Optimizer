
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.logger import db_logger
from database.db_models import Base


# PostgreSQL database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


# Database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# FastAPI database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Initialize database tables
def init_db():
    try:
        Base.metadata.create_all(bind=engine)

        db_logger.info(
            "PostgreSQL tables initialized successfully"
        )

    except Exception:
        db_logger.exception(
            "Database initialization failed"
        )
        raise


# Test database connectivity
def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception:
        db_logger.exception(
            "Database connection failed"
        )
        return False
