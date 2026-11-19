from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from legko.settings import get_settings


def _ensure_sqlite_parent(db_url: str) -> None:
    if not db_url.startswith("sqlite:///"):
        return
    path = db_url.removeprefix("sqlite:///")
    if path in (":memory:",):
        return
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = Path.cwd() / file_path
    file_path.parent.mkdir(parents=True, exist_ok=True)


@event.listens_for(Engine, "connect")
def _sqlite_pragma(dbapi_connection, connection_record) -> None:
    if dbapi_connection.__class__.__module__.startswith("sqlite3"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def make_engine():
    settings = get_settings()
    _ensure_sqlite_parent(settings.database_url)
    return create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}
        if settings.database_url.startswith("sqlite")
        else {},
    )


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()