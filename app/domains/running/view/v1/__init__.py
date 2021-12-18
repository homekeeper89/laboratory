from flask import request
from app.domains import main_api
from flasgger import swag_from
from app.domains.running.use_case.create_running_use_case import CreateRunningUseCase
from app.domains.running.use_case.participate_running_use_case import ParticipateRunningUseCase
from app.domains.running.use_case.get_participants_use_case import GetParticipantsUseCase
from app.core.decorator import make_http_response
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from app.domains.running.use_case.get_runnings_use_case import GetRunningsUseCase
from flask import abort

from pydantic import BaseModel, ValidationError
from app.domains.running.schema.v1_schema import (
    CreateParticipationRequestSchema,
    CreateRunningSchema,
    GetRunningsRequestSchema,
)


def validator(original_class):
    orig_init = original_class.__init__
    # Make copy of original __init__, so we can call it without recursion
    def __init__(self, **args):
        try:
            orig_init(self, **args)  # Call the original __init__
        except ValidationError as ve:
            print(ve)
            abort(400, ve.errors())

    original_class.__init__ = __init__  # Set the class' __init__ to the new one
    return original_class


@validator
class BaseRequestModel(BaseModel):
    pass


class QueryModel(BaseModel):
    age: int


class RequestBodyModel(BaseRequestModel):
    some: str
    end: str


@main_api.route("/running/body_model", methods=["POST"])
@make_http_response(200)
def get_body_model():
    body = RequestBodyModel(**request.json)
    return {"data": "success"}


@main_api.route("/running/query_model")
@make_http_response(200)
def get_query_model():
    kk = QueryModel(**request.args)
    return {"data": "success"}


@main_api.route("/running/v1/<string:mode>")
@jwt_required()
@make_http_response(200)
@swag_from("get_runnings.yml")
def get_runnings(mode: str):
    data = request.json
    data = GetRunningsRequestSchema(mode=mode, offset=data.get("offset"))
    return GetRunningsUseCase().execute(data.mode, data.offset)


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
    data = CreateParticipationRequestSchema(**data)
    user_id = get_jwt_identity()
    return ParticipateRunningUseCase().execute(data.running_id, user_id, data.invite_code)


@main_api.route("/running/v1", methods=["POST"])
@jwt_required()
@make_http_response(200)
@swag_from("create_running.yml")
def create_running():
    data = request.json
    dto = CreateRunningSchema(**data)
    dto.user_id = get_jwt_identity()
    return CreateRunningUseCase().execute(dto)
