from abc import ABCMeta, abstractmethod
import requests
from app.core.exceptions import FailOuterApiResponseException


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

    def validate_token(self) -> bool:
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {self.token}"}
        res = requests.get(url, headers=headers)
        if not res.ok:
            raise FailOuterApiResponseException(f"status_code: {res.status_code}")

        return True
