from flask.json import jsonify
from app.domains.running.dto import CreateRoomData, RunningConfigData
from app.domains.running.enum import RunningModeEnum


class CreateRoomUseCase:
    def __init__(self):
        pass

    def execute(self, dto: CreateRoomData):
        try:
            if not self.__validate_config(dto.mode, dto.config):
                raise AssertionError(f"wrong_mode: {dto.mode}")
            # room 생성
            # room id 생성
        except AssertionError as e:
            print(f"wrong_config {e.args}")
            # TODO jsonify 여기서 제거
            return jsonify(data={"message": f"wrong_config_or_mode: {dto}"}, meta={}), 409

        return jsonify(data={"room_id": 12345}, meta={"category": dto.category, "mode": dto.mode})

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
