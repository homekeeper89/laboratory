from app.utils.social_login import BaseSocialLoginHelper
from app.core.exceptions import (
    FailUseCaseLogicException,
    ThirdPartyCommunicationException,
    UnexpectedDataException,
)
from flask_jwt_extended import create_access_token


class ValidateAccessTokenUseCase:
    def __init__(self):
        pass

    def execute(self, category: str, token: str):
        social_helper = self.__get_helper(category, token)
        try:
            user_data = social_helper.parsing_data()
            token = create_access_token(identity=user_data)
        except ThirdPartyCommunicationException as ure:
            print(f"{ure.msg}")
            return {"error": ure, "desc": f"{category} api_fail"}
        except UnexpectedDataException as ude:
            print(f"{ude.msg}")
            return {"error": ude, "desc": f"fail_parsing_data_from {category}"}
        except FailUseCaseLogicException as fe:
            return {"error": fe, "desc": fe.msg}

        data = {"access_token": token}
        meta = {"category": category}
        return {"data": data, "meta": meta}

    def __get_helper(self, category: str, token: str):
        for helper_cls in BaseSocialLoginHelper.__subclasses__():
            try:
                if helper_cls.is_matched_category(category):
                    return helper_cls(category, token)
            except KeyError:
                raise FailUseCaseLogicException(msg=f"{category} has_no_helper")
