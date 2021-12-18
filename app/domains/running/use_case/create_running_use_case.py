from typing import Optional
import uuid
from app.domains.running.enum import RunningCategoryEnum, RunningModeEnum, RunningStatusEnum
from app.domains.running.repository.running_repository import RunningRepository
from app.core.exceptions import FailUseCaseLogicException


class CreateRunningUseCase:
    def __init__(self):
        self.__running_repo = RunningRepository()

    def execute(self, dto):
        try:
            if not self.__validate_config(dto.mode, dto.config):
                raise AssertionError(f"wrong_mode: {dto.mode}")

            self.__is_user_valid_status(dto.user_id)

            invite_code = self.__make_invite_code(dto.category)
            running_id = self.__running_repo.create_running(
                dto.user_id, dto.category, dto.mode, invite_code, dto.config
            )
        except FailUseCaseLogicException:
            return {"data": {"message": f"has_ready_status_running: {dto}"}, "meta": {}}

        except AssertionError as e:
            print(f"wrong_config {e.args}")
            return {"data": {"message": f"wrong_config_or_mode: {dto}"}, "meta": {}}

        return {
            "data": {"running_id": running_id, "invite_code": invite_code},
            "meta": {"category": dto.category, "mode": dto.mode},
        }

    def __is_user_valid_status(self, user_id: int):
        invalid_status_list = RunningStatusEnum.get_invalid_status()
        record = self.__running_repo.get_running_records_by_user_id(user_id, invalid_status_list)
        if record:
            raise FailUseCaseLogicException

    def __make_invite_code(self, category: RunningCategoryEnum) -> Optional[str]:
        if category == RunningCategoryEnum.PUBLIC:
            return None
        return str(uuid.uuid4()).split("-")[0]

    def __validate_config(self, mode: str, config):
        res = False
        assert_msg = f"mode_and_config_not_valid mode: {mode}, config: {config}"
        if mode == RunningModeEnum.COMPETITION:
            assert config.distance, assert_msg
            res = True
            config.limit_user_counts = None
            config.limit_minutes = None

        if mode == RunningModeEnum.FREE:
            assert config.limit_user_counts and config.limit_minutes, assert_msg
            res = True
            config.distance = None

        return res
