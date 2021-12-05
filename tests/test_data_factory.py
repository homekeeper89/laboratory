import pytest

from app.core.database.models import Running, RunningParticipant, User

from app.domains.running.enum import RunningModeEnum
from app.core.database.models import Running


def test_running_factory_should_make(session, running_domain_factory):
    running_domain_factory(4, running_mode=RunningModeEnum.COMPETITION)

    res = session.query(Running).all()
    assert res[0].mode == "COMPETITION"


@pytest.mark.xfail
def test_custom_build_fixture_with_param_should_work(session, running_domain_factory):
    res = running_domain_factory(1, Running__status="kk")
    res = session.query(Running).filter(Running.id == res.id).first()
    assert res.status == "kk"


def test_custom_build_fixture_should_work(session, running_domain_factory):
    res = running_domain_factory(4)
    running_id = res.id

    assert running_id
    assert session.query(User).count() == 4
    assert (
        session.query(RunningParticipant)
        .filter(RunningParticipant.running_id == running_id)
        .count()
        == 4
    )


def test_running_should_make_record(session, running_factory):
    record = running_factory.build()
    session.add(record)
    session.commit()
    assert record.id

    running_factory.create()
    res = session.query(Running).first()
    assert res

    running_factory.create_batch(10)
    cnt = session.query(Running).count()

    assert cnt >= 10
