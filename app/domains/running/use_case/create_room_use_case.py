from flask.json import jsonify
from app.domains.running.dto import CreateRoomData


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
            # TODO
            return jsonify(data={"message": f"wrong_config_or_mode: {dto}"}, meta={}), 409

        return jsonify(data={"room_id": 12345}, meta={"category": dto.category, "mode": dto.mode})

    def __validate_config(self, mode: str, config: dict):
        # TODO enum 으로 추상화 하기
        res = False
        assert_msg = f"mode_and_config_not_valid mode: {mode}, config: {config}"
        if mode == "competition":
            distance = config.get("distance", None)
            assert distance, assert_msg
            res = True

        if mode == "free":
            counts = config.get("limit_user_counts", None)
            minutes = config.get("limit_minutes", None)
            assert counts and minutes, assert_msg
            res = True

        return res
