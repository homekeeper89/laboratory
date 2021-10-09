from app.utils.social_login import BaseSocialLoginHelper


class ValidateAccessTokenUseCase:
    def __init__(self):
        pass

    def execute(self, category: str, token: str):

        social_helper = self.__get_helper(category, token)
        valid_token = social_helper.validate_token()

        return "SUCCESS"

    def __get_helper(self, category: str, token: str):
        for helper_cls in BaseSocialLoginHelper.__subclasses__():
            try:
                if helper_cls.is_matched_category(category):
                    return helper_cls(category, token)
            except KeyError:
                print(f"{category} has_no_helper")
                return ""
