import pytest
from app.domains.running.use_case.create_room_use_case import CreateRoomUseCase
from app.domains.running.dto import RunningConfigData
from app.domains.running.enum import RunningModeEnum


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
