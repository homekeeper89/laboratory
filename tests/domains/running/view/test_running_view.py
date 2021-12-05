import json
from app.core.database.models import Running
from app.domains.running.enum import RunningStatusEnum, RunningModeEnum, RunningCategoryEnum


def test_get_runnings_with_wrong_category_should_return_400(
    session, get_token_headers, test_client, running_domain_factory
):
    headers = get_token_headers(1234)
    running_mode = "wrong"
    endpoint = f"/api/running/v1/{running_mode}"

    res = test_client.get(endpoint, headers=headers)
    assert res.status_code == 400


def test_get_runnings_should_return_200(
    session, get_token_headers, test_client, running_domain_factory
):
    running_domain_factory(
        4, running_mode=RunningModeEnum.COMPETITION, running_category=RunningCategoryEnum.PUBLIC
    )
    headers = get_token_headers(1234)
    running_mode = RunningModeEnum.COMPETITION.lower()
    endpoint = f"/api/running/v1/{running_mode}"

    data = {"offset": 3}

    res = test_client.get(endpoint, json=data, headers=headers)
    assert res.status_code == 200
    data = res.json["data"]

    assert data


def test_get_running_info_with_not_joined_user_should_return_409(
    session,
    get_jwt_token,
    test_client,
    running_domain_factory,
):
    user_id = 1234
    running = running_domain_factory(4)
    token = get_jwt_token(user_id)
    endpoint = f"/api/running/v1/{running.id}"
    res = test_client.get(endpoint, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 409


def test_invalid_running_should_return_409(session, test_client, get_token_headers, get_jwt_token):
    session.add(
        Running(user_id=1234, status=RunningStatusEnum.IN_PROGRESS, category="cat", mode="mode")
    )
    session.commit()
    running_id = 1
    endpoint = f"/api/running/v1/participation"
    headers = get_token_headers(1234)

    data = {"running_id": running_id}
    res = test_client.post(endpoint, data=json.dumps(data), headers=headers)
    assert res.status_code == 409


def test_none_running_should_return_404(session, test_client, get_token_headers, get_jwt_token):
    running_id = 1234
    endpoint = f"/api/running/v1/participation"
    headers = get_token_headers(1234)

    data = {"running_id": running_id}
    res = test_client.post(endpoint, data=json.dumps(data), headers=headers)
    assert res.status_code == 404


def test_create_room_should_return_running_id(
    session, test_client, get_token_headers, get_jwt_token
):
    endpoint = "/api/running/v1"
    data = {
        "category": "private",  # open
        "mode": "competition",  # free
        "config": {"distance": 123},
    }
    headers = get_token_headers(1234)

    res = test_client.post(endpoint, data=json.dumps(data), headers=headers)

    assert res.status_code == 200
    data = res.json["data"]
    assert data
    meta = res.json["meta"]
    assert meta["category"]
    assert meta["mode"]
