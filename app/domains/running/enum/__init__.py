from app.base.base_enum import BaseEnum
from enum import auto


class RunningCategoryEnum(BaseEnum):
    """
    방 종류 결정, 이를 바탕으로 public 여부가 결정됨
    """

    PRIVATE = auto()
    PUBLIC = auto()


class RunningModeEnum(BaseEnum):
    """
    방 생성시의 모드, 방 내부 구성원들과의 인터랙션을 결정함
    """

    COMPETITION = auto()
    FREE = auto()
