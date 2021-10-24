from app.domains.running.use_case.participate_running_use_case import ParticipateRunningUseCase
import pytest
from app.domains.running.enum import RunningStatusEnum
from app.core.database.models import Running, RunningParticipant


def test_private_running_with_none_code_should_return_fail(session):
    code = "code"
    session.add(
        Running(
            user_id=1234,
            status=RunningStatusEnum.ATTENDING,
            category="cat",
            mode="mode",
            invite_code=code,
        )
    )
    session.commit()
    running_id = 1

    uc = ParticipateRunningUseCase()
    res = uc.execute(running_id, 1234, "not_code")
    assert res["error"]


def test_uc_should_make_record(session):
    session.add(
        Running(user_id=1234, status=RunningStatusEnum.ATTENDING, category="cat", mode="mode")
    )
    session.commit()

    running_id = 1
    uc = ParticipateRunningUseCase()
    uc.execute(running_id, 1234)

    res = (
        session.query(RunningParticipant)
        .filter(RunningParticipant.running_id == running_id)
        .first()
    )
    assert res


@pytest.mark.parametrize(
    "status", [(RunningStatusEnum.IN_PROGRESS), (RunningStatusEnum.TERMINATED)]
)
def test_invalid_status_running_should_return_fail(session, status):
    session.add(Running(user_id=1234, status=status, category="cat", mode="mode"))
    session.commit()

    running_id = 1
    uc = ParticipateRunningUseCase()
    res = uc.execute(running_id, 1234)

    assert res["error"]


def test_participate_none_running_should_return_fail(session):
    running_id = 1234
    uc = ParticipateRunningUseCase()
    res = uc.execute(running_id, 1234)
    assert res["error"]
    assert str(running_id) in res["desc"]
