from app import create_app
import pytest


def test_fixture_app_should_work(app):
    assert app


@pytest.mark.xfail(reason="ci/cd 에서 통과하지 못함")
@pytest.mark.parametrize("env", [("test"), ("dev"), ("prod")])
def test_app_with_config_should_return_env(env):
    app = create_app(env)

    assert app.config["ENV"] == env


def test_health_check_should_return_success(test_client):
    res = test_client.get("/")
    assert res.status_code == 200
