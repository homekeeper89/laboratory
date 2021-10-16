from flask import request
from app import socketio
from flask_socketio import emit, join_room, leave_room, send
from flask import request
import json

@socketio.on('disconnect', namespace="/running")
def on_disconnect():
    print("disconnected")

@socketio.on("send_gps_data", namespace="/running")
def on_room_event(data):
    room_id = data.pop("room_id")
    # name, args:List 형태
    data["lat"]="abc"
    data["lot"]="bbc"
    emit("calc_data", data, room=room_id)

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