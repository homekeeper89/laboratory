from pydantic.dataclasses import dataclass
from pydantic import validator
from app.domains.running.enum import RunningCategoryEnum, RunningModeEnum


@dataclass
class CalcDistanceData:
    from_data: tuple = (0, 0)
    to_data: tuple = (0, 0)
    distance: int = 0


@dataclass
class CreateRoomData:
    user_id: str = ""
    category: RunningCategoryEnum = RunningCategoryEnum.PRIVATE
    mode: RunningModeEnum = RunningModeEnum.COMPETITION
    config: dict = None
