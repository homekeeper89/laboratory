import pytest
from app import create_app


@pytest.fixture(scope="session")
def app():

    app = create_app("test")
    app_context = app.app_context()
    app_context.push()

    yield app

    app_context.pop()
