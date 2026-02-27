from sqlalchemy import create_engine, text
from app.config import settings

# Create synchronous engine for MS SQL Server
# MS SQL Server doesn't play well with most async drivers for SQLAlchemy Core yet
engine = create_engine(
    settings.sqlalchemy_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

def get_connection():
    """Context manager for obtaining a database connection."""
    with engine.connect() as connection:
        yield connection
        # The connection is automatically closed when the context manager exits.
        # SQLAlchemy connection objects in Core handle transaction commits if configured, 
        # or we can manually commit within the repository.
