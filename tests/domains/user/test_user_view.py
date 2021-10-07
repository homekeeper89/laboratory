def test_view_call_should_return_success(test_client):
    res = test_client.get("/api/user/v1/ping")

    assert res.status_code == 200
