from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings
import os

# Create database directory if not exists
os.makedirs(settings.upload_dir, exist_ok=True)

# Select database URL based on configuration
if settings.db_type.lower() == "mysql":
    database_url = settings.database_url_mysql
else:
    database_url = settings.database_url_pg

# Create engine
engine = create_engine(
    database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
