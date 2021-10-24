from app.domains.running.enum import RunningStatusEnum
from app.domains.running.repository.running_repository import RunningRepository
from app.core.exceptions import InvalidStatusException, RepoException


class ParticipateRunningUseCase:
    def __init__(self):
        self.__running_repo = RunningRepository()

    def execute(self, running_id: int, user_id: int, invite_code: str = None):
        try:
            running = self.__running_repo.get_record_by_id(running_id)
            assert running, f"running: {running_id} not_exists"
            self.__is_valid_status(running, invite_code)
            self.__running_repo.create_running_participant(running_id, user_id)
        except RepoException:
            return {"error": "internal_error", "desc": f"running: {running_id} user_id: {user_id}"}

        except InvalidStatusException as ie:
            return {"error": "invalid_status", "desc": ie.msg}

        except AssertionError as ae:
            return {"error": "not_exists", "desc": ae.args[0]}

        return {
            "data": {"message": "success"},
            "meta": {},
        }

    def __is_valid_status(self, running, invite_code: str = None):
        status = running.status
        invalid_status_list = [
            RunningStatusEnum.TERMINATED.name,
            RunningStatusEnum.IN_PROGRESS.name,
        ]
        if status in invalid_status_list:
            raise InvalidStatusException(
                msg=f"running: {running.id} invalid_stats: {running.status}"
            )
        if running.invite_code and running.invite_code != invite_code:
            raise InvalidStatusException(
                msg=f"running: {running.id} invite_code_not_correct: {invite_code}"
            )
