import pytest
from . import RunningFactory, RunningParticipantFactory, UserFactory


@pytest.fixture(scope="function")
def running_domain_factory(session):
    def _running_domain_factory(user_counts: int = 4, **kwargs):
        nonlocal session
        res = RunningFactory.build()
        session.add(res)
        session.flush()

        models = RunningParticipantFactory.build_batch(user_counts, running_id=res.id)
        session.add_all(models)
        session.flush()

        for model in models:
            user = UserFactory(id=model.user_id)
            session.add(user)
        session.commit()
        return res

    return _running_domain_factory
