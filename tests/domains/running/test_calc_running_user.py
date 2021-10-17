import json


def test_running_socket_should_calc_distance(app, socket_app, get_round_data):
    running_namespace = "/running/v1"
    first_user = socket_app.test_client(app, namespace=running_namespace)

    first_user.get_received(running_namespace)

    join_room = "join_room"
    unique_room_id = "some_unique_id"
    first_user.emit(join_room, {"room_id": unique_room_id}, namespace=running_namespace)
    first_user.get_received(running_namespace)

    data = {"room_id": unique_room_id, "from_data": (0, 0), "to_data": (0, 0), "distance": 0}

    first_user.emit("send_gps_data", data, namespace=running_namespace)
    data = first_user.get_received(running_namespace)
    assert data[0]["name"] == "calc_data"

    distance = 0
    for index, to_data in enumerate(get_round_data[1:]):
        from_data = get_round_data[index]
        data = {
            "user_id": "unique_user_id",
            "room_id": unique_room_id,
            "from_data": from_data,
            "to_data": to_data,
            "distance": distance,
        }
        first_user.emit("send_gps_data", data, namespace=running_namespace)
        data = first_user.get_received(running_namespace)
        calc_data = data[0]["args"][0]["data"]["distance"]
        distance = calc_data
    assert distance >= 180
