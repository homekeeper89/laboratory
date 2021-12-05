from app.domains.running.use_case.get_runnings_use_case import GetRunningsUseCase
from app.domains.running.enum import RunningCategoryEnum, RunningModeEnum

from jsonschema import validate

running_schema = {
    "type": "object",
    "properties": {
        "meta": {"type": "object"},
        "configs": {"type": "array"},
    },
}


def test_uc_with_public_running_should_return_data(session, running_domain_factory):
    running_domain_factory(
        4, running_mode=RunningModeEnum.COMPETITION, running_category=RunningCategoryEnum.PUBLIC
    )
    running_domain_factory(
        4, running_mode=RunningModeEnum.COMPETITION, running_category=RunningCategoryEnum.PUBLIC
    )
    running_domain_factory(
        4, running_mode=RunningModeEnum.COMPETITION, running_category=RunningCategoryEnum.PUBLIC
    )

    mode = RunningModeEnum.COMPETITION
    uc = GetRunningsUseCase()
    limit_count = 3
    res = uc.execute(mode, limit_count)
    assert len(res["data"][0].keys()) == limit_count
    running = res["data"][0][1]
    validate(instance=running, schema=running_schema)


def test_uc_with_private_running_should_return_null(session, running_domain_factory):
    running_domain_factory(
        4, running_mode=RunningModeEnum.COMPETITION, running_category=RunningCategoryEnum.PRIVATE
    )

    category = RunningCategoryEnum.PRIVATE
    uc = GetRunningsUseCase()
    limit_count = 3
    res = uc.execute(category, limit_count)

    assert not res["data"]
