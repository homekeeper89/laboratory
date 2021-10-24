from flask import request
from app.domains import main_api
from flasgger import swag_from
from app.domains.running.use_case.create_running_use_case import CreateRunningUseCase
from app.domains.running.dto import CreateRunningData


@main_api.route("/running/v1/room", methods=["POST"])
@swag_from("create_running.yml")
def create_running():
    data = request.json
    # TODO request validation 만들어야함
    dto = CreateRunningData().make(**data)
    return CreateRunningUseCase().execute(dto)
