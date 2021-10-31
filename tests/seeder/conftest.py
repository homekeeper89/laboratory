import pytest

from app.domains.running.enum import RunningStatusEnum
from . import RunningFactory, RunningParticipantFactory, UserFactory


@pytest.fixture(scope="function")
def running_domain_factory(session):
    def _running_domain_factory(user_counts: int = 4, **kwargs):
        nonlocal session
        res = RunningFactory.build(status=RunningStatusEnum.ATTENDING.name)
        session.add(res)
        session.flush()

        model = RunningParticipantFactory.build(running_id=res.id, user_id=res.user_id)
        try:
            models = RunningParticipantFactory.build_batch(user_counts - 1, running_id=res.id)
            models.append(model)
        except Exception:
            models = [model]

        session.add_all(models)
        session.flush()

        for model in models:
            user = UserFactory(id=model.user_id)
            session.add(user)
        session.commit()
        return res

    return _running_domain_factory
