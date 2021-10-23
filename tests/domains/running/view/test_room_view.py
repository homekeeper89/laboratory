import json
import pytest


def test_create_room_should_return_room_id(test_client, get_json_headers):
    endpoint = "/api/running/v1/room"
    data = {
        "category": "private",  # open
        "mode": "competition",  # free
        "config": {"distance": 123},
    }

    res = test_client.post(endpoint, data=json.dumps(data), headers=get_json_headers)

    assert res.status_code == 200
    data = res.json["data"]
    assert data
    meta = res.json["meta"]
    assert meta["category"]
    assert meta["mode"]
