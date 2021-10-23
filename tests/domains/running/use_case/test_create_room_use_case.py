import pytest
from app.domains.running.use_case.create_room_use_case import CreateRoomUseCase
from app.domains.running.dto import CreateRoomData, RunningConfigData
from app.domains.running.enum import RunningCategoryEnum, RunningModeEnum, RunningStatusEnum
from app.core.database.models import Running


def test_ready_running_user_should_not_make_running(session):
    dto = CreateRoomData(user_id=1234, category=RunningCategoryEnum.PUBLIC)
    CreateRoomUseCase().execute(dto)

    uc_res = CreateRoomUseCase().execute(dto)
    assert uc_res["data"]["message"]


def test_use_case_with_public_mode_should_not_make_invite_code(session):
    dto = CreateRoomData(user_id=12345, category=RunningCategoryEnum.PUBLIC)
    uc_res = CreateRoomUseCase().execute(dto)

    res = session.query(Running).filter(Running.user_id == dto.user_id).first()
    assert not uc_res["data"]["invite_code"]
    assert not res.invite_code


def test_use_case_should_make_room_and_status_is_waiting(session):
    dto = CreateRoomData(user_id=1234)
    uc_res = CreateRoomUseCase().execute(dto)

    res = session.query(Running).filter(Running.user_id == dto.user_id).first()
    assert res
    assert uc_res["data"]["room_id"] == res.id
    assert res.status == RunningStatusEnum.WAITING


@pytest.mark.parametrize(
    "mode, config, expected",
    [
        (RunningModeEnum.COMPETITION, RunningConfigData(distance=123), True),
        (RunningModeEnum.FREE, RunningConfigData(limit_user_counts=5), True),
    ],
)
def test_validate_mode_should_return_expected(mode, config, expected):
    uc = CreateRoomUseCase()
    res = uc._CreateRoomUseCase__validate_config(mode, config)
    assert res == expected
