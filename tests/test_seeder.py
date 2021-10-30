from app.core.database.models import Running, RunningParticipant, User


def test_custom_build_fixture_should_work(session, factory_session, running_domain_factory):
    res = factory_session(running_domain_factory.build(RunningParticipant=4))

    assert res.id
    assert session.query(User).count() == 4

    res = factory_session(running_domain_factory.build_batch(4, RunningParticipant=4))
    assert res


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


def test_parameters_should_work(session, running_participant_factory):
    running_participant_factory.create_batch(10, running_id=1234, status=10)
    res = session.query(RunningParticipant).filter(RunningParticipant.running_id == 1234).all()
    assert len(res) == 10


def test_domain_factory_should_make_related_data(session, running_domain_factory):
    counts = 4
    running_domain_factory.create_batch(1, RunningParticipant=counts)

    assert session.query(User).count() == counts
    assert session.query(Running).count() == 1
