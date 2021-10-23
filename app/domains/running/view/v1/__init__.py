from flask import request
from app.domains import main_api
from flasgger import swag_from
from app.domains.running.use_case.create_room_use_case import CreateRoomUseCase
from app.domains.running.dto import CreateRoomData


@main_api.route("/running/v1/room", methods=["POST"])
@swag_from("create_room.yml")
def create_room():
    data = request.json
    # TODO request validation 만들어야함
    dto = CreateRoomData().make(**data)
    return CreateRoomUseCase().execute(dto)
