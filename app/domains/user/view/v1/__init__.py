from app.domains import main_api
from flasgger import swag_from
from flask import request

from app.domains.user.use_case.v1.validate_access_token_use_case import ValidateAccessTokenUseCase
from app.core.decorator import make_http_response


@main_api.route("/user/v1/ping")
@swag_from("temp_ping.yml")
def temp_ping():
    return "SUCCESS"


@main_api.route("/user/v1/token", methods=["POST"])
@make_http_response(200)
@swag_from("create_token.yml")
def create_token():
    data = request.json
    category = data.get("category")
    token = data.get("access_token")

    return ValidateAccessTokenUseCase().execute(category, token)
