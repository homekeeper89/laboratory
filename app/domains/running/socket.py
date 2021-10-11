from flask import request
from flask import session
from app import socketio
from flask_socketio import emit, join_room, leave_room, send
from flask import Flask, session, request, json as flask_json
import json


@socketio.on("send_gps_data", namespace="/running")
def on_room_event(data):
    room_id = data.pop("room_id")
    # name, args:List 형태
    data["lat"]="abc"
    data["lot"]="bbc"
    emit("calc_data", data, room=room_id)


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


@socketio.event(namespace="/test")
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


@socketio.on("join room")
def on_join_room(data):
    room = data["room"]
    print(f"room {room}", request.sid)
    join_room(data["room"])


@socketio.on("leave room")
def on_leave_room(data):
    leave_room(data["room"])


@socketio.on("join room", namespace="/test")
def on_join_room_namespace(data):
    join_room(data["room"])


@socketio.on("leave room", namespace="/test")
def on_leave_room_namespace(data):
    leave_room(data["room"])


@socketio.on("my room event")
def on_room_event(data):
    room = data.pop("room")
    print(f"custom_room {room}", request.sid)
    # name, args:List 형태
    emit("my room response", data, room=room)


@socketio.on("my room namespace event", namespace="/test")
def on_room_namespace_event(data):
    room = data.pop("room")
    send("room message", room=room)


@socketio.on("connect")
def on_connect(auth):
    if auth != {"foo": "bar"}:  # pragma: no cover
        return False
    if request.args.get("fail"):
        return False
    send("connected")
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


@socketio.on("message")
def handle_message(data):
    print("received message: " + data)


@socketio.on("message")
def handle_message(message):
    send(message)
    print(">>>", message)


@socketio.on("json")
def handle_json(json):
    send(json, json=True, broadcast=True)
    print("json", json)


@socketio.on("my custom event")
def handle_my_custom_event(json):
    emit("my custom response", json)
    print("emit", json)


@socketio.on("message", namespace="/test")
def on_message_test(message):
    send(message)


@socketio.on("my custom broadcast namespace event", namespace="/test")
def on_custom_event_broadcast_test(data):
    emit("my custom namespace response", data, namespace="/test", broadcast=True)
