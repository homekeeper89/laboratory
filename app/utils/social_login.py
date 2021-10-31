from abc import ABCMeta, abstractmethod
import requests
from app.core.exceptions import ThirdPartyCommunicationException, UnexpectedDataException
import random
from flask import current_app


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
    def parsing_primary_data(self):
        """각 social data 에서 유저를 특정 지을 수 있는 정보(id 등)을 parsing 한다"""
        pass


class DevTestLoginHelder(BaseSocialLoginHelper):
    @staticmethod
    def is_matched_category(category) -> bool:
        return category == "dev_test_env"

    def validate_token(self) -> dict:
        if self.token == current_app.config.get("DEV_ACCESS_TOKEN", None):
            return {"id": random.randint(1, 10000)}

    def parsing_primary_data(self):
        data = self.validate_token()
        try:
            return data["id"]
        except KeyError as ke:
            print(f"wrong_data_response: {data} error: {ke}")
            raise UnexpectedDataException("parsing_fail")


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

    def parsing_primary_data(self):
        data = self.validate_token()
        try:
            return data["id"]
        except KeyError as ke:
            print(f"wrong_data_response: {data} error: {ke}")
            raise UnexpectedDataException("parsing_fail")
