from app.domains.running.use_case.get_participants_use_case import GetParticipantsUseCase


def test_use_case_with_no_user_should_return_error_res():
    uc = GetParticipantsUseCase()
    res = uc.execute(1, 2)

    assert res["error"]


def test_use_case_should_return_data(session, running_domain_factory):
    users = 4
    running = running_domain_factory(users)

    uc = GetParticipantsUseCase()
    res = uc.execute(running.id, running.user_id)
    assert len(res["data"]["users"]) == users

    user = res["data"]["users"][0]
    assert user["nickname"]
    assert user["running_status"]

    running = res["data"]["running"]
    assert running["status"]
