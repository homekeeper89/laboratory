from app.core.database.models import Running


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
