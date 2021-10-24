import pytest
from app.domains.running.dto import CreateRunningData, RunningConfigData
from pydantic.error_wrappers import ValidationError
from app.domains.running.enum import RunningCategoryEnum, RunningModeEnum


def test_dict_init_should_make_data_dto():
    data = {
        "category": "private",  # open
        "mode": "competition",  # free
        "config": {"distance": 123},
    }
    data = CreateRunningData().make(**data)
    assert data.category == RunningCategoryEnum.PRIVATE


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
        CreateRunningData(123, category, mode, config)


def test_room_dto_should_not_raise_error():
    config_data = RunningConfigData(10, 10, 5)
    assert CreateRunningData(123, "PRIVATE", "COMPETITION", config_data)
