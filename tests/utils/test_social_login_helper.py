import pytest
from app.utils.social_login import KakaoLoginHelper
from app.core.exceptions import FailOuterApiResponseException


def test_kakao_validate_token_with_not_success_should_raise_error(requests_mock):
    requests_mock.get("https://kapi.kakao.com/v2/user/me", text="data", status_code=401)

    with pytest.raises(FailOuterApiResponseException):
        token = "some_token"
        kcs = KakaoLoginHelper("kakao", token)
        kcs.validate_token()


@pytest.mark.parametrize("category, expected", [("kakao", True), ("apple", False)])
def test_kakao_helper_should_return_true(category, expected):
    token = "some_token"

    kcs = KakaoLoginHelper(category, token)
    res = kcs.is_matched_category(category)
    assert res == expected
