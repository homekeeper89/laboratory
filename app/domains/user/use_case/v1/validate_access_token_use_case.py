from app.utils.social_login import BaseSocialLoginHelper
from app.core.exceptions import UnexpectedApiResponseException, UnexpectedDataException
from flask_jwt_extended import create_access_token
from flask import jsonify


class ValidateAccessTokenUseCase:
    def __init__(self):
        pass

    def execute(self, category: str, token: str):
        social_helper = self.__get_helper(category, token)
        try:
            user_data = social_helper.parsing_data()
            token = create_access_token(identity=user_data)
        except UnexpectedApiResponseException as ure:
            # TODO fail response 표준 규격 만들기
            print(f"{ure.msg}")
            return (
                jsonify(error=f"fail_commuicate_to_target_server, may_be_given_token_is_weird"),
                401,
            )
        except UnexpectedDataException as ude:
            print(f"{ude.msg}")
            return jsonify(error=f"fail_to_parse_data"), 409

        # TODO success response 표준 규격 만들기
        data = {"access_token": token}
        meta = {"category": category}
        return jsonify(data=data, meta=meta)

    def __get_helper(self, category: str, token: str):
        for helper_cls in BaseSocialLoginHelper.__subclasses__():
            try:
                if helper_cls.is_matched_category(category):
                    return helper_cls(category, token)
            except KeyError:
                print(f"{category} has_no_helper")
                return ""
