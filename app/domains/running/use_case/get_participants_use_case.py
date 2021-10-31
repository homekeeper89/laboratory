from app.domains.running.repository.running_repository import RunningRepository
from app.core.exceptions import FailUseCaseLogicException, RepoException
from flask import current_app


class GetParticipantsUseCase:
    def __init__(self):
        self.__running_repo = RunningRepository()

    def execute(self, running_id: int, user_id: int):
        try:
            running_users = self.__running_repo.get_running_with_users(running_id)
            if not running_users:
                raise FailUseCaseLogicException(msg=f"running: {running_id} has_no_users")

            data = {}
            data["running"] = self.__parse_running_data(running_users[0].Running)
            data["users"] = self.__parse_users(running_users)
        except RepoException as re:
            return {"error": re, "desc": f"running: {running_id} user_id: {user_id}"}

        except FailUseCaseLogicException as ie:
            return {"error": ie, "desc": ie.msg}

        return {
            "data": data,
            "meta": {"max_user_counts": current_app.config["POLICY"].get("LIMIT_USER_COUNTS")},
        }

    def __parse_users(self, running_users):
        # TODO entity 도입시 수정
        data = []
        for user in running_users:
            temp = {}
            temp["id"] = user.User.id
            temp["nickname"] = user.User.nickname
            temp["running_status"] = user.RunningParticipant.status
            temp["is_host"] = user.Running.user_id == user.User.id
            data.append(temp)
        return data

    def __parse_running_data(self, running):
        return {"id": running.id, "status": running.status, "user_id": running.user_id}
