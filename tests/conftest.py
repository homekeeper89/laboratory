from _pytest.main import Session
import pytest
from app import create_app


@pytest.fixture(scope="session")
def app():

    app = create_app("test")
    app_context = app.app_context()
    app_context.push()

    yield app

    app_context.pop()


@pytest.fixture(scope="session")
def test_client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def get_json_headers():
    return {"Content-Type": "application/json"}
