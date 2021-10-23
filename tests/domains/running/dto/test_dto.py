import pytest
from app.domains.running.dto import CreateRoomData
from pydantic.error_wrappers import ValidationError
from app.domains.running.enum import RunningCategoryEnum, RunningModeEnum


@pytest.mark.parametrize(
    "category, mode, config", [("kk", "kk", {}), (RunningCategoryEnum.PRIVATE, "kk", {})]
)
def test_wrong_parameter_should_raise_error(category, mode, config):
    with pytest.raises(ValidationError):
        CreateRoomData(123, category, mode, config)


def test_room_dto_should_not_raise_error():
    assert CreateRoomData(123, "PRIVATE", "COMPETITION", {})
