"""Database session management."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True,  # Verify the connection before using it
    pool_recycle=3600,    # Recycle connections after 1 hour
    pool_size=5,         # Number of connections to keep open
    max_overflow=10,     # Number of connections to create if pool is exhausted
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,  # Prevent attribute refresh issues
)

# Base class for declarative models
Base = declarative_base()


def get_db() -> SessionLocal:
    """
    Dependency function that yields database sessions.
    
    Yields:
        Session: A database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
