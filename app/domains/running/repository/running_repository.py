from app.core.database import session
from app.core.database.models import Running
from app.core.exceptions import RepoException
from app.domains.running.enum import RunningStatusEnum


class RunningRepository:
    def get_record_by_user_id(self, user_id: int):
        try:
            return session.query(Running).filter(Running.user_id == user_id).first()
        except Exception as e:
            print(e)
            raise RepoException(msg="unexpected_error_occur")

    def create_running(
        self,
        user_id: int,
        category: str,
        mode: str,
        invite_code: str,
        status: str = RunningStatusEnum.WAITING,
    ) -> int:
        try:
            model = Running(
                user_id=user_id,
                category=category,
                mode=mode,
                invite_code=invite_code,
                status=status,
            )
            session.add(model)
            session.commit()
            session.refresh(model)

            return model.id
        except Exception as e:
            session.rollback()
            session.flush()
            print(e)
            raise RepoException(msg="unexpected_error_occur")
