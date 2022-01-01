import pytest
from app import create_app
from app.core.database import db as _db


@pytest.fixture(scope="session")
def lab_app():
    app = create_app("lab")
    app_context = app.app_context()
    app_context.push()

    yield app

    app_context.pop()


@pytest.fixture(scope="function")
def lab_db(lab_app):
    _db.app = lab_app
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope="function")
def lab_session(lab_db):
    """Creates a new database session for each test, rolling back changes afterwards"""
    yield lab_db.session
    lab_db.session.rollback()
    lab_db.session.close()
    lab_db.session.remove()
