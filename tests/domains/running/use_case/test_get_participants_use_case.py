from app.domains.running.use_case.get_participants_use_case import GetParticipantsUseCase


def test_use_case_should_return_data(session, running_participant_factory):
    running_id = 1234
    user_id = 123
    users = 5
    running_participant_factory.create_batch(users, running_id=running_id, user_id=user_id)

    uc = GetParticipantsUseCase()
    res = uc.execute(running_id, user_id)

    assert len(res["data"]) == users
