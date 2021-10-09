import json


def test_get_token_should_return_success(test_client, get_json_headers):
    endopoint = "/api/user/v1/token"
    data = {"category": "kakao", "access_token": "token_given_by"}
    res = test_client.post(endopoint, data=json.dumps(data), headers=get_json_headers)

    assert res.status_code == 200
