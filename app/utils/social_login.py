from abc import ABCMeta, abstractmethod


class BaseSocialLoginHelper(metaclass=ABCMeta):
    def __init__(self, category: str, token: str):
        self.category = category
        self.token = token

    @staticmethod
    def is_matched_category(category: str) -> bool:
        return False

    @abstractmethod
    def validate_token(self):
        pass


class KakaoLoginHelper(BaseSocialLoginHelper):
    @staticmethod
    def is_matched_category(category) -> bool:
        return category == "kakao"

    def validate_token(self):
        return self.token
