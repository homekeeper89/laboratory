import pytest
from app import create_app, socketio
from app.core.database import db as _db


@pytest.fixture(scope="session")
def app():
    app = create_app("test")
    app_context = app.app_context()
    app_context.push()

    yield app

    app_context.pop()


@pytest.fixture(scope="function")
def db(app):
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


from app.core.database.models import Running


@pytest.fixture(scope="function")
def session(db):
    """Creates a new database session for each test, rolling back changes afterwards"""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session  # 1번 상황을 위한 세팅

    yield session  # 2번 상황을 위한 세팅
    transaction.rollback()
    connection.close()
    session.remove()


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


@pytest.fixture
def get_round_data():
    # 약 200m 데이터
    return [
        (37.355422, 126.936847),
        (37.355435, 126.936721),
        (37.355435, 126.936539),
        (37.355350, 126.936346),
        (37.355235, 126.936207),
        (37.355116, 126.936127),
        (37.354971, 126.935993),
        (37.354805, 126.935867),
        (37.354688, 126.935770),
        (37.354581, 126.935690),
        (37.354481, 126.935634),
        (37.354406, 126.935623),
        (37.354310, 126.935626),
        (37.354229, 126.935656),
        (37.354088, 126.935731),
    ]
