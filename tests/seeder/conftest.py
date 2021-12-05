import pytest

from app.domains.running.enum import (
    RunningCategoryEnum,
    RunningModeEnum,
    RunningStatusEnum,
    RunningConfigCategoryEnum,
)
from . import RunningFactory, RunningParticipantFactory, UserFactory, RunningConfigFactory


def make_models_by_category(mode: RunningModeEnum, running_id: int):
    if mode == RunningModeEnum.COMPETITION:
        return [
            RunningConfigFactory.build(
                category=RunningConfigCategoryEnum.DISTANCE, running_id=running_id
            )
        ]
    else:
        return [
            RunningConfigFactory.build(
                category=RunningConfigCategoryEnum.LIMIT_MINUTES, running_id=running_id
            ),
            [
                RunningConfigFactory.build(
                    category=RunningConfigCategoryEnum.LIMIT_USER_COUNTS, running_id=running_id
                )
            ],
        ]


@pytest.fixture(scope="function")
def running_domain_factory(session):
    def _running_domain_factory(user_counts: int = 4, **kwargs):
        nonlocal session
        mode = kwargs.get("running_mode", RunningModeEnum.COMPETITION)
        category = kwargs.get("running_category", RunningCategoryEnum.PRIVATE)
        running = RunningFactory.build(
            status=RunningStatusEnum.ATTENDING.name, mode=mode, category=category
        )
        session.add(running)
        session.flush()
        model = RunningParticipantFactory.build(running_id=running.id, user_id=running.user_id)
        try:
            models = RunningParticipantFactory.build_batch(user_counts - 1, running_id=running.id)
            models.append(model)
        except Exception:
            models = [model]

        config_models = make_models_by_category(mode, running.id)
        session.add_all(models)
        session.add_all(config_models)
        session.flush()

        for model in models:
            user = UserFactory(id=model.user_id)
            session.add(user)
        session.commit()
        return running

    return _running_domain_factory
