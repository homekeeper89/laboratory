from app.utils.social_login import BaseSocialLoginHelper
from app.core.exceptions import FailOuterApiResponseException


class ValidateAccessTokenUseCase:
    def __init__(self):
        pass

    def execute(self, category: str, token: str):
        social_helper = self.__get_helper(category, token)
        try:
            valid_token = social_helper.validate_token()
        except FailOuterApiResponseException as fe:
            print(f"{fe.msg}")
            return "Fail"

        return "SUCCESS"

    def __get_helper(self, category: str, token: str):
        for helper_cls in BaseSocialLoginHelper.__subclasses__():
            try:
                if helper_cls.is_matched_category(category):
                    return helper_cls(category, token)
            except KeyError:
                print(f"{category} has_no_helper")
                return ""
