import pytest
from app.domains.running.use_case.create_running_use_case import CreateRunningUseCase
from app.domains.running.schema.v1_schema import RunningConfingSchema, CreateRunningSchema
from app.domains.running.enum import (
    RunningCategoryEnum,
    RunningModeEnum,
    RunningParticipantEnum,
    RunningStatusEnum,
)
from app.core.database.models import Running, RunningParticipant, RunningConfig
from app.core.exceptions import FailUseCaseLogicException


@pytest.mark.parametrize(
    "mode, data, expected",
    [
        (RunningModeEnum.COMPETITION, {"distance": 600}, 1),
        (RunningModeEnum.FREE, {"limit_user_counts": 10, "limit_minutes": 10}, 2),
    ],
)
def test_create_room_should_make_config(session, mode, data, expected):
    dto = CreateRunningSchema(user_id=1234, mode=mode, config=data)
    res = CreateRunningUseCase().execute(dto)
    running_id = res["data"]["running_id"]

    res = session.query(RunningConfig).filter(RunningConfig.running_id == running_id).count()
    assert res == expected


def test_create_room_should_make_join(session):
    dto = CreateRunningSchema(user_id=1234, category=RunningCategoryEnum.PUBLIC)
    CreateRunningUseCase().execute(dto)

    res = (
        session.query(RunningParticipant).filter(RunningParticipant.user_id == dto.user_id).first()
    )
    assert res.status == RunningParticipantEnum.WAITING


@pytest.mark.parametrize(
    "status",
    [(RunningStatusEnum.IN_PROGRESS), (RunningStatusEnum.ATTENDING)],
)
def test_create_running_with_invalid_status_should_raise(session, status):
    user_id = 1212
    session.add(Running(user_id=1212, category="cat", mode="md", status=status))
    session.commit()

    uc = CreateRunningUseCase()
    with pytest.raises(FailUseCaseLogicException):
        uc._CreateRunningUseCase__is_user_valid_status(user_id)


def test_ready_running_user_should_not_make_running(session):
    dto = CreateRunningSchema(user_id=1234, category=RunningCategoryEnum.PUBLIC)
    CreateRunningUseCase().execute(dto)

    uc_res = CreateRunningUseCase().execute(dto)
    assert uc_res["data"]["message"]


def test_use_case_with_public_mode_should_not_make_invite_code(session):
    dto = CreateRunningSchema(user_id=12345, category=RunningCategoryEnum.PUBLIC)
    uc_res = CreateRunningUseCase().execute(dto)

    res = session.query(Running).filter(Running.user_id == dto.user_id).first()
    assert not uc_res["data"]["invite_code"]
    assert not res.invite_code


def test_use_case_should_make_room_and_status_is_attending(session):
    dto = CreateRunningSchema(user_id=1234)
    uc_res = CreateRunningUseCase().execute(dto)

    res = session.query(Running).filter(Running.user_id == dto.user_id).first()
    assert res
    assert uc_res["data"]["running_id"] == res.id
    assert res.status == RunningStatusEnum.ATTENDING


@pytest.mark.parametrize(
    "mode, config, expected",
    [
        (RunningModeEnum.COMPETITION, RunningConfingSchema(distance=123), True),
        (RunningModeEnum.FREE, RunningConfingSchema(limit_user_counts=5), True),
    ],
)
def test_validate_mode_should_return_expected(mode, config, expected):
    uc = CreateRunningUseCase()
    res = uc._CreateRunningUseCase__validate_config(mode, config)
    assert res == expected
