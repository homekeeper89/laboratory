from app.core.database.models import Running, RunningParticipant


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
