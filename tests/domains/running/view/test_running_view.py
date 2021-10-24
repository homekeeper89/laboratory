import json
from app.core.database.models import Running
from app.domains.running.enum import RunningStatusEnum


def test_invalid_running_should_return_409(session, test_client, get_json_headers):
    session.add(
        Running(user_id=1234, status=RunningStatusEnum.IN_PROGRESS, category="cat", mode="mode")
    )
    session.commit()
    running_id = 1
    endpoint = f"/api/running/v1/participation"

    data = {"running_id": running_id}
    res = test_client.post(endpoint, data=json.dumps(data), headers=get_json_headers)
    assert res.status_code == 409


def test_none_running_should_return_404(session, test_client, get_json_headers):
    running_id = 1234
    endpoint = f"/api/running/v1/participation"

    data = {"running_id": running_id}
    res = test_client.post(endpoint, data=json.dumps(data), headers=get_json_headers)
    assert res.status_code == 404


def test_create_room_should_return_running_id(session, test_client, get_json_headers):
    endpoint = "/api/running/v1"
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
