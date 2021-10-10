from flask import session
from app import socketio
from flask_socketio import emit, join_room, leave_room, send
from flask import Flask, session, request, json as flask_json
import json


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


@socketio.on("message", namespace="/test")
def on_message_test(message):
    send(message)


@socketio.on("my custom broadcast namespace event", namespace="/test")
def on_custom_event_broadcast_test(data):
    emit("my custom namespace response", data, namespace="/test", broadcast=True)
