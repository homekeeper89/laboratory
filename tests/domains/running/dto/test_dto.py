import pytest
from app.domains.running.dto import CreateRoomData, RunningConfigData
from pydantic.error_wrappers import ValidationError


@pytest.mark.parametrize(
    "category, mode, config",
    [
        ("kk", "kk", {}),
        ("PRIVATE", "kk", {}),
        ("PRIVATE", "FREE", {"kk": "kk"}),
    ],
)
def test_wrong_parameter_should_raise_error(category, mode, config):
    with pytest.raises(ValidationError):
        CreateRoomData(123, category, mode, config)


def test_room_dto_should_not_raise_error():
    config_data = RunningConfigData(10, 10, 5)
    assert CreateRoomData(123, "PRIVATE", "COMPETITION", config_data)
