import pytest
from app.utils.social_login import KakaoLoginHelper
from app.core.exceptions import ThirdPartyCommunicationException, UnexpectedDataException


def test_parsing_wrong_data_should_raise(requests_mock):
    requests_mock.get("https://kapi.kakao.com/v2/user/me", json={"a": "b"}, status_code=200)
    with pytest.raises(UnexpectedDataException):
        token = "some_token"
        kcs = KakaoLoginHelper("kakao", token)
        kcs.parsing_primary_data()


def test_parsing_data_should_work(requests_mock, sample_kakao_data):
    requests_mock.get("https://kapi.kakao.com/v2/user/me", json=sample_kakao_data, status_code=200)
    category = "kakao"
    token = "some_token"
    kcs = KakaoLoginHelper(category, token)
    res = kcs.parsing_primary_data()
    assert res == sample_kakao_data["id"]


def test_kakao_validate_token_with_not_success_should_raise_error(requests_mock):
    requests_mock.get("https://kapi.kakao.com/v2/user/me", json={"a": "b"}, status_code=401)

    with pytest.raises(ThirdPartyCommunicationException):
        token = "some_token"
        kcs = KakaoLoginHelper("kakao", token)
        kcs.validate_token()


@pytest.mark.parametrize("category, expected", [("kakao", True), ("apple", False)])
def test_kakao_helper_should_return_true(category, expected):
    token = "some_token"

    kcs = KakaoLoginHelper(category, token)
    res = kcs.is_matched_category(category)
    assert res == expected
