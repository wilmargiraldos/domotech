from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_PATH = os.getenv("DOMO_TECH_DB", "data/app.db")
DB_URL = f"sqlite:///{DB_PATH}"

# echo=True can be enabled for debugging
engine = create_engine(DB_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session():
    """Yields a SQLAlchemy session; use with context manager."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
