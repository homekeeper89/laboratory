import pytest


@pytest.fixture(scope="function")
def get_token_data():
    def _get_token_data(category: str = "kakao", access_token: str = "some_token"):

        return {"category": category, "access_token": access_token}

    return _get_token_data
