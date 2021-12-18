from app.core.database import session
from app.core.database.models import Running, RunningConfig, RunningParticipant, User
from app.core.exceptions import RepoException
from app.domains.running.enum import (
    RunningCategoryEnum,
    RunningModeEnum,
    RunningStatusEnum,
    RunningParticipantEnum,
)
from typing import List


class RunningRepository:
    def get_runnings_with_mode(self, mode: RunningModeEnum, offset: int = 4):
        try:
            return (
                session.query(Running, RunningConfig)
                .join(RunningConfig, Running.id == RunningConfig.running_id)
                .filter(Running.mode == mode.upper())
                .filter(Running.category == RunningCategoryEnum.PUBLIC)
                .limit(offset)
                .all()
            )
        except Exception as e:
            print(e)
            raise RepoException(msg="unexpected_error_occur")

    def get_running_with_users(
        self, running_id: int, status: str = RunningStatusEnum.ATTENDING.name
    ):
        try:
            return (
                session.query(RunningParticipant, Running, User)
                .join(Running, RunningParticipant.running_id == Running.id)
                .join(User, RunningParticipant.user_id == User.id)
                .filter(Running.status == status)
                .all()
            )
        except Exception as e:
            print(e)
            raise RepoException(msg="unexpected_error_occur")

    def get_running_record_by_id(self, running_id: int):
        try:
            return session.query(Running).filter(Running.id == running_id).first()
        except Exception as e:
            print(e)
            raise RepoException(msg="unexpected_error_occur")

    def get_running_records_by_user_id(self, user_id: int, status_list: List[str]):
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

    def create_running_participant(
        self, running_id: int, user_id: int, status: str = RunningParticipantEnum.WAITING.name
    ):
        try:
            model = RunningParticipant(running_id=running_id, user_id=user_id, status=status)
            session.add(model)
            session.commit()
        except Exception as e:
            print(e)
            raise RepoException(msg="unexpected_error_occur")

    def create_running(
        self,
        user_id: int,
        category: str,
        mode: str,
        invite_code: str,
        config,
        status: str = RunningStatusEnum.ATTENDING.name,
    ) -> int:
        """
            running 을 생성하면 생성한 사람은 참가자로 포함되어야함.
            running 을 생성하면 해당 달리기의 설정값도 만들어야함

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
                user_id=user_id, running_id=model.id, status=RunningParticipantEnum.WAITING.name
            )
            session.add(rp_model)

            configs = []
            config = config.dict(exclude_none=True)
            for field, value in config.items():
                category = str(field).upper()
                configs.append(RunningConfig(running_id=model.id, category=category, value=value))
            session.add_all(configs)
            session.commit()
            return model.id
        except Exception as e:
            session.rollback()
            session.flush()
            print(e)
            raise RepoException(msg="unexpected_error_occur")
