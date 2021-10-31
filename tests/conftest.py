import pytest
from app import create_app, socketio
from app.core.database import db as _db
from tests.seeder import MODEL_FACTORIES
from tests.seeder.conftest import running_domain_factory
from pytest_factoryboy import register
from flask_jwt_extended import create_access_token


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


@pytest.fixture(scope="function")
def session(db):
    """Creates a new database session for each test, rolling back changes afterwards"""
    set_factories_session(db.session)
    yield db.session
    db.session.rollback()
    db.session.close()
    db.session.remove()


def register_factories():
    # 예시) register(StoreFactory) 이런 형태
    for factory in MODEL_FACTORIES:
        register(factory)


register_factories()


def set_factories_session(session):
    # 예시) UserFactory._meta.sqlalchemy_session = session
    for factory in MODEL_FACTORIES:
        factory._meta.sqlalchemy_session = session


@pytest.fixture(scope="function")
def factory_session(session):
    def _factory_session(factory):
        nonlocal session
        try:
            len(factory)
            session.add_all(factory)
        except TypeError:
            session.add(factory)
        session.commit()
        return factory

    return _factory_session


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


@pytest.fixture(scope="function")
def get_jwt_token(app):
    def _get_jwt_token(user_id: int):
        return create_access_token(identity=user_id)

    return _get_jwt_token


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
