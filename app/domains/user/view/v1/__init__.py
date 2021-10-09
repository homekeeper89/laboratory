from app.domains import main_api
from flasgger import swag_from
from flask import request


@main_api.route("/user/v1/ping")
@swag_from("temp_ping.yml")
def temp_ping():
    return "SUCCESS"


@main_api.route("/user/v1/token", methods=["POST"])
def create_token():
    data = request.json
    return "SUCCESS"
