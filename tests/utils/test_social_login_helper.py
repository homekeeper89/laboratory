import pytest
from app.utils.social_login import KakaoLoginHelper
from app.core.exceptions import UnexpectedApiResponseException, UnexpectedDataException


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


def test_parsing_wrong_data_should_raise(requests_mock):
    requests_mock.get("https://kapi.kakao.com/v2/user/me", json={"a": "b"}, status_code=200)
    with pytest.raises(UnexpectedDataException):
        token = "some_token"
        kcs = KakaoLoginHelper("kakao", token)
        kcs.parsing_data()


def test_parsing_data_should_work(requests_mock, sample_kakao_data):
    requests_mock.get("https://kapi.kakao.com/v2/user/me", json=sample_kakao_data, status_code=200)
    category = "kakao"
    token = "some_token"
    kcs = KakaoLoginHelper(category, token)
    res = kcs.parsing_data()
    assert res == sample_kakao_data["id"]


def test_kakao_validate_token_with_not_success_should_raise_error(requests_mock):
    requests_mock.get("https://kapi.kakao.com/v2/user/me", json={"a": "b"}, status_code=401)

    with pytest.raises(UnexpectedApiResponseException):
        token = "some_token"
        kcs = KakaoLoginHelper("kakao", token)
        kcs.validate_token()


@pytest.mark.parametrize("category, expected", [("kakao", True), ("apple", False)])
def test_kakao_helper_should_return_true(category, expected):
    token = "some_token"

    kcs = KakaoLoginHelper(category, token)
    res = kcs.is_matched_category(category)
    assert res == expected
