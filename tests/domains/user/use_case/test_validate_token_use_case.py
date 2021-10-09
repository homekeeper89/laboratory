from app.domains.user.use_case.v1.validate_access_token_use_case import ValidateAccessTokenUseCase


def test_use_case_should_return_data(app, get_token_data):
    data = get_token_data()
    uc = ValidateAccessTokenUseCase()
    res = uc.execute(data["category"], data["access_token"])
    assert res
