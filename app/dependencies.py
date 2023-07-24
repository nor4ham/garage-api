from sqlalchemy.orm import Session

from app.db.db import SessionLocal


def get_db_session():
    session: Session = SessionLocal()
    try:
        with session.begin():
            yield session
    except Exception:
        session.rollback()
    finally:
        session.close()
