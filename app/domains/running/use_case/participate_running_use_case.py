from app.domains.running.enum import RunningStatusEnum
from app.domains.running.repository.running_repository import RunningRepository
from app.core.exceptions import FailUseCaseLogicException, RepoException, NotFoundException


class ParticipateRunningUseCase:
    # TODO 인원제한 확인 로직 추가
    def __init__(self):
        self.__running_repo = RunningRepository()

    def execute(self, running_id: int, user_id: int, invite_code: str = None):
        try:
            running = self.__running_repo.get_record_by_id(running_id)
            if not running:
                raise NotFoundException(msg=f"running_id: {running_id}")
            self.__is_valid_status(running, invite_code)
            self.__running_repo.create_running_participant(running_id, user_id)
        except RepoException as re:
            return {"error": re, "desc": f"running: {running_id} user_id: {user_id}"}

        except FailUseCaseLogicException as ie:
            return {"error": ie, "desc": ie.msg}

        except NotFoundException as ae:
            return {"error": ae, "desc": ae.msg}

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
            raise FailUseCaseLogicException(
                msg=f"running: {running.id} is_invalid_status: {running.status}"
            )
        if running.invite_code and running.invite_code != invite_code:
            raise FailUseCaseLogicException(
                msg=f"running: {running.id} invite_code_not_correct: {invite_code}"
            )
