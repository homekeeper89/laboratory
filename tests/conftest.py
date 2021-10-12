import pytest
from app import create_app, socketio


@pytest.fixture(scope="session")
def app():
    app = create_app("test")
    app_context = app.app_context()
    app_context.push()

    yield app

    app_context.pop()


@pytest.fixture(scope="session")
def socket_app(app):
    socketio.init_app(app)
    yield socketio


@pytest.fixture(scope="session")
def test_client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def get_json_headers():
    return {"Content-Type": "application/json"}


@pytest.fixture
def sample_kakao_data():
    # NOTE https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#req-user-info 참고
    # nickname 만 동의한 상황
    return {
        "id": 123456789,
        "kakao_account": {
            "profile_nickname_needs_agreement": False,
            "profile": {"nickname": "홍길동"},
        },
        "properties": {
            "nickname": "홍길동카톡",
            "custom_field1": "23",
            "custom_field2": "여",
        },
    }
