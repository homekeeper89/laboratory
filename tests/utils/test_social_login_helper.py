import pytest
from app.utils.social_login import KakaoLoginHelper


@pytest.mark.parametrize("category, expected", [("kakao", True), ("apple", False)])
def test_kakao_helper_should_return_true(category, expected):
    token = "some_token"

    kcs = KakaoLoginHelper(category, token)
    res = kcs.is_matched_category(category)
    assert res == expected

    res = kcs.validate_token()
    assert res == token
