# NOTE https://github.com/miguelgrinberg/Flask-socket_app/blob/main/test_socket_app.py
# NOTE https://blog.naver.com/PostView.nhn?isHttpsRedirect=true&blogId=shino1025&logNo=222179697262&parentCategoryNo=&categoryNo=33&viewDate=&isShowPopularPosts=true&from=search
import json


def test_leaving_room_should_share_message(app, socket_app):
    running_namespace = "/running/v1"
    first_user = socket_app.test_client(app, namespace=running_namespace)
    second_user = socket_app.test_client(app, namespace=running_namespace)

    first_user.get_received(running_namespace)
    second_user.get_received(running_namespace)

    join_room = "join_room"
    unique_room_id = "some_unique_id"
    first_user.emit(join_room, {"room_id": unique_room_id}, namespace=running_namespace)
    second_user.emit(join_room, {"room_id": unique_room_id}, namespace=running_namespace)
    first_user.get_received(running_namespace)
    second_user.get_received(running_namespace)

    data = {"room_id": unique_room_id, "lat": 12345, "lot": 123}
    first_user.emit("leave_room", data, namespace=running_namespace)
    res = second_user.get_received(running_namespace)
    assert res


def test_each_user_should_share_data(app, socket_app):
    running_namespace = "/running/v1"
    first_user = socket_app.test_client(app, namespace=running_namespace)
    second_user = socket_app.test_client(app, namespace=running_namespace)

    first_user.get_received(running_namespace)
    second_user.get_received(running_namespace)

    join_room = "join_room"
    unique_room_id = "some_unique_id"
    first_user.emit(join_room, {"room_id": unique_room_id}, namespace=running_namespace)
    second_user.emit(join_room, {"room_id": unique_room_id}, namespace=running_namespace)
    first_user.get_received(running_namespace)
    second_user.get_received(running_namespace)

    data = {"room_id": unique_room_id, "lat": 12345, "lot": 123}
    first_user.emit("send_gps_data", data, namespace=running_namespace)
    data = second_user.get_received(running_namespace)
    assert data[0]["name"] == "calc_data"

    data = first_user.get_received(running_namespace)
    assert data[0]["name"] == "calc_data"


def test_each_user_should_join_room(app, socket_app):
    running_namespace = "/running/v1"
    first_user = socket_app.test_client(app, namespace=running_namespace)
    second_user = socket_app.test_client(app, namespace=running_namespace)

    first_user.get_received(running_namespace)
    second_user.get_received(running_namespace)

    join_room = "join_room"
    unique_room_id = "some_unique_id"
    first_user.emit(join_room, {"room_id": unique_room_id}, namespace=running_namespace)
    second_user.emit(join_room, {"room_id": unique_room_id}, namespace=running_namespace)

    received = first_user.get_received(running_namespace)
    assert received[0]["name"] == "join_room_success"


def test_each_user_should_connected_running_rooms(app, socket_app):
    running_namespace = "/running/v1"
    first_user = socket_app.test_client(app, namespace=running_namespace)
    second_user = socket_app.test_client(app, namespace=running_namespace)

    data = first_user.get_received(running_namespace)

    args = json.loads(data[0]["args"])
    assert args["status"] == 200
    data = second_user.get_received(running_namespace)
    args = json.loads(data[0]["args"])
    assert args["status"] == 200
