from app.domains.running.repository.running_repository import RunningRepository
from app.core.database.models import Running


def test_create_record_should_make_record_and_return_id(session):
    repo = RunningRepository()
    record_id = repo.create_running(123, "kk", "kk", "kk", "kk")
    assert type(record_id) == int

    rec = session.query(Running).first()
    assert rec.status == "kk"
    assert record_id == rec.id
