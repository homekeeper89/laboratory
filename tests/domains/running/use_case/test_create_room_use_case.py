import pytest
from app.domains.running.use_case.create_room_use_case import CreateRoomUseCase
from app.domains.running.dto import CreateRoomData


@pytest.mark.parametrize(
    "mode, config, expected",
    [
        ("competition", {"distance": 123}, True),
        ("free", {"limit_user_counts": 5, "limit_minutes": 10}, True),
    ],
)
def test_validate_mode_should_return_expected(mode, config, expected):
    uc = CreateRoomUseCase()
    res = uc._CreateRoomUseCase__validate_config(mode, config)
    assert res == expected


def test_wrong_mode_should_return_message(app):
    dto = CreateRoomData(category="kk", mode="kk", config={"kk": "kk"})
    uc = CreateRoomUseCase()
    res = uc.execute(dto)
    assert res[0].json["data"]["message"]
