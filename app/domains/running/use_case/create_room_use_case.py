from typing import Optional
import uuid
from app.domains.running.dto import CreateRoomData, RunningConfigData
from app.domains.running.enum import RunningCategoryEnum, RunningModeEnum, RunningStatusEnum
from app.domains.running.repository.running_repository import RunningRepository
from app.core.exceptions import AlreadyStatusException


class CreateRoomUseCase:
    def __init__(self):
        self.__running_repo = RunningRepository()

    def execute(self, dto: CreateRoomData):
        try:
            if not self.__validate_config(dto.mode, dto.config):
                raise AssertionError(f"wrong_mode: {dto.mode}")

            self.__has_user_ready_running(dto.user_id)

            invite_code = self.__make_invite_code(dto.category)
            room_id = self.__running_repo.create_running(
                dto.user_id, dto.category, dto.mode, invite_code
            )
        except AlreadyStatusException:
            return {"data": {"message": f"has_ready_status_running: {dto}"}, "meta": {}}

        except AssertionError as e:
            print(f"wrong_config {e.args}")
            return {"data": {"message": f"wrong_config_or_mode: {dto}"}, "meta": {}}

        return {
            "data": {"room_id": room_id, "invite_code": invite_code},
            "meta": {"category": dto.category, "mode": dto.mode},
        }

    def __has_user_ready_running(self, user_id: int):
        record = self.__running_repo.get_record_by_user_id(user_id)
        if getattr(record, "status", None) == RunningStatusEnum.WAITING:
            raise AlreadyStatusException

    def __make_invite_code(self, category: RunningCategoryEnum) -> Optional[str]:
        if category == RunningCategoryEnum.PUBLIC:
            return None
        return str(uuid.uuid4()).split("-")[0]

    def __validate_config(self, mode: str, config: RunningConfigData):
        res = False
        assert_msg = f"mode_and_config_not_valid mode: {mode}, config: {config}"
        if mode == RunningModeEnum.COMPETITION:
            assert config.distance, assert_msg
            res = True

        if mode == RunningModeEnum.FREE:
            assert config.limit_user_counts and config.limit_minutes, assert_msg
            res = True

        return res
