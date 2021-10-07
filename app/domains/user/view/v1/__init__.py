from app.domains import main_api


@main_api.route("/user/v1/ping")
def temp_ping():
    return "SUCCESS"
