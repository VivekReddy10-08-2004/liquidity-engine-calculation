"""Engine and transaction-scoped session helpers."""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.app.config import Settings


def create_session_factory(settings: Settings | None = None) -> sessionmaker[Session]:
    resolved = settings or Settings()
    engine = create_engine(resolved.database_url, pool_pre_ping=True)
    return sessionmaker(bind=engine, expire_on_commit=False)


def session_scope(factory: sessionmaker[Session]) -> Iterator[Session]:
    """Yield a session with commit/rollback behavior suitable for API dependencies."""
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
