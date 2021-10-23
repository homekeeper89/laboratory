from app import socketio
from flask_socketio import emit, join_room, leave_room, send
import json

from flask_socketio import emit
from app.domains.running.use_case.calculate_distance_use_case import CalculateDistanceUseCase
from app.domains.running.dto import CalcDistanceData

# TODO class-based 로 변경해야함
def make_response(data: dict, meta: dict, status: int = 200) -> dict:
    # TODO json 체체화 이슈 존재
    return {
        "status": status,
        "data": data,
        "meta": meta,
    }


# NOTE : 메서드 명은 connect 로 되어야함
@socketio.event(namespace="/running/v1")
def connect():
    try:
        response = make_response({}, {"message": "success"})
        send(json.dumps(response))
    except Exception as e:
        print(f"connect_socket_error: {e.args}")
        response = make_response({}, {"message": "error_occur"}, 400)
        send(json.dumps(response))


@socketio.on("disconnect", namespace="/running/v1")
def on_disconnect():
    try:
        response = make_response({}, {"message": "success"})
        send(json.dumps(response))
    except Exception as e:
        print(f"connect_socket_error: {e.args}")
        response = make_response({}, {"message": "error_occur"}, 400)
        send(json.dumps(response))


@socketio.on("send_gps_data", namespace="/running/v1")
def on_room_event(data):
    running_id = data.pop("running_id")
    user_id = data.get("user_unique_id")

    uc = CalculateDistanceUseCase()
    from_data = tuple(data.get("from_data", [0, 0]))
    to_data = tuple(data.get("to_data", [0, 0]))
    distance = data.get("distance", 0)

    dto = CalcDistanceData(from_data=from_data, to_data=to_data, distance=distance)
    calc_distance = uc.execute(dto)
    data = {
        "distance": calc_distance,
        "user_id": user_id,
    }
    meta = {"message": "success"}
    response = make_response(data, meta)
    emit("calc_data", response, room=running_id)


@socketio.on("leave_room", namespace="/running/v1")
def on_leave_room_namespace(data):
    running_id = data.get("running_id", 0)
    # TODO room counts 줄이기
    try:
        leave_room(data["running_id"])
        response = make_response({}, {}, 200)
        emit("leave_room_success", response, room=running_id)
    except Exception as e:
        print(f"leave_room_error: {e.args}")
        response = make_response({}, {"message": "error_occur"}, 400)
        send(json.dumps(response))


@socketio.on("join_room", namespace="/running/v1")
def on_join_room_namespace(data):
    running_id = data.get("running_id", 0)
    # 해당 running_id 의 상태 확인
    # 인원 & 상태
    try:
        join_room(data["running_id"])
        response = make_response({}, {}, 200)
        emit("join_room_success", response, room=running_id)
    except Exception as e:
        print(f"join_room_error: {e.args}")
        response = make_response({}, {"message": "error_occur"}, 400)
        send(json.dumps(response))


@socketio.on_error("/running/v1")  # handles the '/chat' namespace
def error_handler_chat(e):
    # e는 raise 혹은 캐치한 에러 그대로 <class 'ValueError'>
    pass
