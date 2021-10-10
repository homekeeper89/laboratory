import json


def test_get_token_should_return_success(
    test_client, requests_mock, get_json_headers, sample_kakao_data
):
    requests_mock.get("https://kapi.kakao.com/v2/user/me", json=sample_kakao_data, status_code=200)
    endopoint = "/api/user/v1/token"
    data = {"category": "kakao", "access_token": "token_given_by"}
    res = test_client.post(endopoint, data=json.dumps(data), headers=get_json_headers)
    data = res.json["data"]
    
    assert res.status_code == 200
    assert data["access_token"]
