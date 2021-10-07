from app.domains import main_api
from flasgger import swag_from


@main_api.route("/user/v1/ping")
@swag_from("temp_ping.yml")
def temp_ping():
    return "SUCCESS"
