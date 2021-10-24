from abc import ABCMeta, abstractmethod
import requests
from app.core.exceptions import ThirdPartyCommunicationException, UnexpectedDataException


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

    @abstractmethod
    def parsing_data(self):
        pass


class KakaoLoginHelper(BaseSocialLoginHelper):
    @staticmethod
    def is_matched_category(category) -> bool:
        return category == "kakao"

    def validate_token(self) -> dict:
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {self.token}"}
        res = requests.get(url, headers=headers)
        if not res.ok:
            raise ThirdPartyCommunicationException(f"status_code: {res.status_code}, {res.text}")
        return res.json()

    def parsing_data(self):
        data = self.validate_token()
        try:
            return data["id"]
        except KeyError as ke:
            print(f"wrong_data_response: {data} error: {ke}")
            raise UnexpectedDataException("parsing_fail")
