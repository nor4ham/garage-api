import pytest
from fastapi.testclient import TestClient
from app.db.db import SessionLocal , engine
from app.dependencies import get_db_session
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.orm import scoped_session

from app.config import config
from app.main import app

ScopedSession = scoped_session(SessionLocal, scopefunc=lambda: "")


def get_db_session_overwrite():
    test_session = ScopedSession()
    test_session.expire_all()
    try:
        with test_session.begin_nested():
            yield test_session
    except Exception as e:
        import logging

        logging.exception(e, exc_info=True)


@pytest.fixture(autouse=True)
def transaction_managementt():
    db_connection = engine.connect()
    db_connection.begin()
    ScopedSession(bind=db_connection)
    yield
    ScopedSession.remove()
    db_connection.close()


@pytest.fixture()
def session():
    return ScopedSession()


@pytest.fixture(scope="session")
def client():
    """
    Create a Postgres database for the tests, and drop it when the tests are done.
    Creates s3 buckets and clears them after the tests are done.
    """

    app.dependency_overrides[get_db_session] = get_db_session_overwrite

    janitor = DatabaseJanitor(
        user=config.DB_USER,
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        version=96,
        password=config.DB_PASSWORD,
    )
    # create the db
    try:
        janitor.init()
    except Exception as e:
        print(e)

    # create all the tables
    from app.api.users import models  # noqa
    from app.db.db import Base

    Base.metadata.create_all(engine)

    yield TestClient(app)

    engine.dispose()
    janitor.drop()
