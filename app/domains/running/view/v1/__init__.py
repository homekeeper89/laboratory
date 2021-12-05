from flask import request
from app.domains import main_api
from flasgger import swag_from
from app.domains.running.use_case.create_running_use_case import CreateRunningUseCase
from app.domains.running.dto import CreateRunningData
from app.domains.running.use_case.participate_running_use_case import ParticipateRunningUseCase
from app.domains.running.use_case.get_participants_use_case import GetParticipantsUseCase
from app.domains.running.enum import RunningModeEnum
from app.core.decorator import make_http_response
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from app.core.exceptions import InvalidRequestException
from app.domains.running.use_case.get_runnings_use_case import GetRunningsUseCase


@main_api.route("/running/v1/<string:mode>")
@jwt_required()
@make_http_response(200)
@swag_from("get_runnings.yml")
def get_runnings(mode: str):
    if not RunningModeEnum.has_value(mode):
        return {"error": InvalidRequestException, "desc": f"category: {mode}"}
    data = request.json
    offset = data.get("offset", 3)
    return GetRunningsUseCase().execute(mode, offset)


@main_api.route("/running/v1/<int:running_id>")
@jwt_required()
@make_http_response(200)
@swag_from("get_running.yml")
def get_running(running_id: int):
    user_id = get_jwt_identity()
    return GetParticipantsUseCase().execute(running_id, user_id)


@main_api.route("/running/v1/participation", methods=["POST"])
@jwt_required()
@make_http_response(200)
@swag_from("participate_running.yml")
def participate_running():
    data = request.json
    # TODO request validation 만들어야함
    running_id = data.get("running_id", None)
    user_id = get_jwt_identity()
    invite_code = str(data.get("invite_code", None))
    return ParticipateRunningUseCase().execute(running_id, user_id, invite_code)


@main_api.route("/running/v1", methods=["POST"])
@jwt_required()
@make_http_response(200)
@swag_from("create_running.yml")
def create_running():
    data = request.json
    # TODO request validation 만들어야함
    dto = CreateRunningData().make(**data)
    dto.user_id = get_jwt_identity()
    return CreateRunningUseCase().execute(dto)
