from app.domains.running.repository.running_repository import RunningRepository
from app.core.database.models import Running


def test_create_record_should_make_record(session):
    repo = RunningRepository()
    res = repo.create_running(123, "kk", "kk", "kk", "kk")

    assert res

    rec = session.query(Running).first()
    assert rec.status == "kk"
