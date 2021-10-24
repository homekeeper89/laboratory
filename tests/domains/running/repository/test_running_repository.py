from app.domains.running.enum import RunningStatusEnum
from app.domains.running.repository.running_repository import RunningRepository
from app.core.database.models import Running


def test_create_record_should_make_record_and_return_id(session):
    repo = RunningRepository()
    record_id = repo.create_running(123, "kk", "kk", "kk")
    assert type(record_id) == int

    rec = session.query(Running).filter(Running.user_id == 123).first()
    assert rec.status == RunningStatusEnum.ATTENDING
    assert record_id == rec.id
