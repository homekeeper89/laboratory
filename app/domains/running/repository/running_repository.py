from app.core.database import session
from app.core.database.models import Running, RunningParticipant
from app.core.exceptions import RepoException
from app.domains.running.enum import RunningStatusEnum, RunningParticipantEnum
from typing import List


class RunningRepository:
    def get_records_by_user_id(self, user_id: int, status_list: List[str]):
        try:
            return (
                session.query(Running)
                .filter(Running.user_id == user_id)
                .filter(Running.status.in_(status_list))
                .all()
            )
        except Exception as e:
            print(e)
            raise RepoException(msg="unexpected_error_occur")

    def create_running(
        self,
        user_id: int,
        category: str,
        mode: str,
        invite_code: str,
        status: str = RunningStatusEnum.ATTENDING,
    ) -> int:
        """running 을 생성하면 생성한 사람은 참가자로 포함되어야함.

        Returns:
            int: 생성한 running id
        """
        try:
            model = Running(
                user_id=user_id,
                category=category,
                mode=mode,
                invite_code=invite_code,
                status=status,
            )
            session.add(model)
            session.flush()

            rp_model = RunningParticipant(
                user_id=user_id, running_id=model.id, status=RunningParticipantEnum.WAITING
            )
            session.add(rp_model)
            session.commit()
            return model.id
        except Exception as e:
            session.rollback()
            session.flush()
            print(e)
            raise RepoException(msg="unexpected_error_occur")
