import pytest

from app.domains.running.enum import RunningModeEnum, RunningStatusEnum, RunningConfigCategoryEnum
from . import RunningFactory, RunningParticipantFactory, UserFactory, RunningConfigFactory


def make_models_by_category(mode: RunningModeEnum):
    if mode == RunningModeEnum.COMPETITION:
        return [RunningConfigFactory.build(category=RunningConfigCategoryEnum.DISTANCE)]
    else:
        return [
            RunningConfigFactory.build(category=RunningConfigCategoryEnum.LIMIT_MINUTES),
            [RunningConfigFactory.build(category=RunningConfigCategoryEnum.LIMIT_USER_COUNTS)],
        ]


@pytest.fixture(scope="function")
def running_domain_factory(session):
    def _running_domain_factory(user_counts: int = 4, **kwargs):
        nonlocal session
        mode = kwargs.get("running_mode", RunningModeEnum.COMPETITION)
        res = RunningFactory.build(status=RunningStatusEnum.ATTENDING.name, mode=mode)
        session.add(res)
        session.flush()

        model = RunningParticipantFactory.build(running_id=res.id, user_id=res.user_id)
        try:
            models = RunningParticipantFactory.build_batch(user_counts - 1, running_id=res.id)
            models.append(model)
        except Exception:
            models = [model]

        config_models = make_models_by_category(mode)
        session.add_all(models)
        session.add_all(config_models)
        session.flush()

        for model in models:
            user = UserFactory(id=model.user_id)
            session.add(user)
        session.commit()
        return res

    return _running_domain_factory
