from flask import request
from app import socketio
from flask_socketio import emit, join_room, leave_room, send
from flask import request
import json

from flask_socketio import emit
from app.domains.running.use_case.calculate_distance_use_case import CalculateDistanceUseCase
from app.domains.running.dto import CalcDistanceData


# TODO class-based 로 변경해야함

# NOTE : 메서드 명은 connect 로 되어야함
@socketio.event(namespace="/running")
def connect():
    send("connected-test")
    send(json.dumps(request.args.to_dict(flat=False)))
    send(
        json.dumps(
            {
                h: request.headers[h]
                for h in request.headers.keys()
                if h not in ["Host", "Content-Type", "Content-Length"]
            }
        )
    )


@socketio.on("disconnect", namespace="/running")
def on_disconnect():
    print("disconnected")


@socketio.on("send_gps_data", namespace="/running")
def on_room_event(data):
    room_id = data.pop("room_id")
    user_id = data.get("user_unique_id")

    uc = CalculateDistanceUseCase()
    from_data = tuple(data.get("from_data", [0, 0]))
    to_data = tuple(data.get("to_data", [0, 0]))
    distance = data.get("distance", 0)

    dto = CalcDistanceData(from_data=from_data, to_data=to_data, distance=distance)
    calc_distance = uc.execute(dto)
    status = 200

    response = {
        "status": status,
        "data": {
            "distance": calc_distance,
            "user_id": user_id,
        },
        "meta": {"message": "success"},
    }
    emit("calc_data", response, room=room_id)


@socketio.on("leave_room", namespace="/running")
def on_join_room_namespace(data):
    room_id = data["room_id"]
    leave_room(data["room_id"])
    emit("leave_room_success", data, room=room_id)


@socketio.on("join_room", namespace="/running")
def on_join_room_namespace(data):
    room_id = data["room_id"]
    join_room(data["room_id"])
    emit("joinning_room_success", data, room=room_id)


@socketio.on_error("/running")  # handles the '/chat' namespace
def error_handler_chat(e):
    # e는 raise 혹은 캐치한 에러 그대로 <class 'ValueError'>
    pass
