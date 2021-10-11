# NOTE https://github.com/miguelgrinberg/Flask-socket_app/blob/main/test_socket_app.py

def test_each_user_should_share_data(app, socket_app):
    running_namespace = "/running"    
    first_user = socket_app.test_client(app, namespace=running_namespace)
    second_user = socket_app.test_client(app, namespace=running_namespace)

    first_user.get_received(running_namespace)
    second_user.get_received(running_namespace)

    join_room ="join_room"
    unique_room_id = "some_unique_id"
    first_user.emit(join_room, {"room_id": unique_room_id}, namespace=running_namespace)
    second_user.emit(join_room, {"room_id": unique_room_id}, namespace=running_namespace)
    first_user.get_received(running_namespace)
    second_user.get_received(running_namespace)

    data = {
        "room_id":unique_room_id,
        "lat":12345,
        "lot":123
    }
    first_user.emit("send_gps_data", data, namespace=running_namespace)
    data = second_user.get_received(running_namespace)
    assert data[0]["name"] == "calc_data"

    data = first_user.get_received(running_namespace)
    assert data[0]["name"] == "calc_data"


def test_each_user_should_join_room(app, socket_app):
    running_namespace = "/running"    
    first_user = socket_app.test_client(app, namespace=running_namespace)
    second_user = socket_app.test_client(app, namespace=running_namespace)

    first_user.get_received(running_namespace)
    second_user.get_received(running_namespace)

    join_room ="join_room"
    unique_room_id = "some_unique_id"
    first_user.emit(join_room, {"room_id": unique_room_id}, namespace=running_namespace)
    second_user.emit(join_room, {"room_id": unique_room_id}, namespace=running_namespace)

    received = first_user.get_received(running_namespace)
    assert received[0]["name"] == "joinning_room_success"

def test_each_user_should_connected_running_rooms(app, socket_app):
    running_namespace = "/running"    
    first_user = socket_app.test_client(app, namespace=running_namespace)
    second_user = socket_app.test_client(app, namespace=running_namespace)

    data = first_user.get_received(running_namespace)
    assert data
    data = second_user.get_received(running_namespace)
    assert data


def test_room_should_workd(app, socket_app):
    client1 = socket_app.test_client(app, auth={"foo": "bar"})
    client2 = socket_app.test_client(app, auth={"foo": "bar"})
    client3 = socket_app.test_client(app, namespace="/test")
    client1.get_received()
    client2.get_received()
    res = client3.get_received("/test")

    client1.emit("join room", {"room": "one"})
    client2.emit("join room", {"room": "one"})
    client3.emit("join room", {"room": "one"}, namespace="/test")
    client1.emit("my room event", {"a": "b", "room": "one"})
    received = client1.get_received()
    assert len(received) == 1
    assert len(received[0]["args"]) == 1
    assert received[0]["name"] == "my room response"
    assert received[0]["args"][0]["a"] == "b"
    assert received == client2.get_received()
    print(received)

    received = client3.get_received("/test")
    assert len(received) == 0

    client1.emit("leave room", {"room": "one"})
    client1.emit("my room event", {"a": "b", "room": "one"})
    received = client1.get_received()
    assert len(received) == 0
    received = client2.get_received()
    assert len(received) == 1
    assert len(received[0]["args"]) == 1
    assert received[0]["name"] == "my room response"
    assert received[0]["args"][0]["a"] == "b"
    print("client2", received)
    received = client2.get_received()
    print("client2", received)
    client2.disconnect()

    socket_app.emit("my room event", {"a": "b"}, room="one")
    received = client1.get_received()
    assert len(received) == 0
    received = client3.get_received("/test")
    assert len(received) == 0

    client3.emit("my room namespace event", {"room": "one"}, namespace="/test")
    received = client3.get_received("/test")
    assert len(received) == 1
    assert received[0]["name"] == "message"
    assert received[0]["args"] == "room message"
    socket_app.close_room("one", namespace="/test")
    client3.emit("my room namespace event", {"room": "one"}, namespace="/test")
    received = client3.get_received("/test")
    assert len(received) == 0


def test_socket_should_conneted(app, socket_app):
    client = socket_app.test_client(app, auth={"foo": "bar"})
    client2 = socket_app.test_client(app, auth={"foo": "bar"})
    assert client.is_connected()
    assert client2.is_connected()
    assert client.eio_sid != client2.eio_sid

    received = client.get_received()
    assert len(received) == 3
    assert received[0]["args"] == "connected"

    client.disconnect()
    assert not client.is_connected()
    assert client2.is_connected()
    client2.disconnect()
    assert not client2.is_connected()


def test_send_message_should_received(app, socket_app):
    client = socket_app.test_client(app, auth={"foo": "bar"})
    client.get_received()
    client.send("echo this message back")
    received = client.get_received()
    assert len(received) == 1
    assert received[0]["args"] == "echo this message back"


def test_send_json_should_share_data(app, socket_app):
    client1 = socket_app.test_client(app, auth={"foo": "bar"})
    client2 = socket_app.test_client(app, auth={"foo": "bar"})
    client1.get_received()
    client2.get_received()
    client1.send({"a": "b"}, json=True)
    received = client1.get_received()

    assert len(received) == 1
    assert received[0]["args"]["a"] == "b"
    received = client2.get_received()
    assert len(received) == 1
    assert received[0]["args"]["a"] == "b"


def test_custom_event_should_work(app, socket_app):
    client = socket_app.test_client(app, auth={"foo": "bar"})
    client.get_received()
    client.emit("my custom event", {"a": "b"})
    received = client.get_received()
    assert len(received) == 1
    assert len(received[0]["args"]) == 1
    assert received[0]["name"] == "my custom response"
    assert received[0]["args"][0]["a"] == "b"


def test_broadcast_namespace(app, socket_app):
    client1 = socket_app.test_client(app, namespace="/test")
    client2 = socket_app.test_client(app, namespace="/test")
    client3 = socket_app.test_client(app, auth={"foo": "bar"})
    received = client2.get_received("/test")
    assert len(received) == 3

    client3.get_received()
    client1.emit("my custom broadcast namespace event", {"a": "b"}, namespace="/test")
    received = client2.get_received("/test")

    assert len(received) == 1
    assert len(received[0]["args"]) == 1
    assert received[0]["name"] == "my custom namespace response"
    assert received[0]["args"][0]["a"] == "b"
    assert len(client3.get_received()) == 0
