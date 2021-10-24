from flask import request
from app.domains import main_api
from flasgger import swag_from
from app.domains.running.use_case.create_running_use_case import CreateRunningUseCase
from app.domains.running.dto import CreateRunningData
from app.domains.running.use_case.participate_running_use_case import ParticipateRunningUseCase


@main_api.route("/running/v1/participation", methods=["POST"])
@swag_from("participate_running.yml")
def participate_running():
    data = request.json
    # TODO request validation 만들어야함
    running_id = data.get("running_id", None)
    user_id = 1234
    invite_code = data.get("invite_code", None)
    return ParticipateRunningUseCase().execute(running_id, user_id, invite_code)


@main_api.route("/running/v1", methods=["POST"])
@swag_from("create_running.yml")
def create_running():
    data = request.json
    # TODO request validation 만들어야함
    dto = CreateRunningData().make(**data)
    return CreateRunningUseCase().execute(dto)
