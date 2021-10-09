import pytest
from app.domains.user.use_case.v1.validate_access_token_use_case import ValidateAccessTokenUseCase
from app.utils.social_login import KakaoLoginHelper


@pytest.mark.parametrize("category", [("kakao")])
def test_get_social_helpert_should_return_expected(category):
    uc = ValidateAccessTokenUseCase()
    helper = uc._ValidateAccessTokenUseCase__get_helper(category, "kk")

    assert isinstance(helper, KakaoLoginHelper)


def test_use_case_should_return_data(app, get_token_data):
    data = get_token_data()
    uc = ValidateAccessTokenUseCase()
    res = uc.execute(data["category"], data["access_token"])
    assert res
