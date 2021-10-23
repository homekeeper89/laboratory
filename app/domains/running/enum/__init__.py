from app.base.base_enum import BaseEnum
from enum import auto


class RunningStatusEnum(BaseEnum):
    """
    running 의 상태,
    대기 > 참가 > 진행 > 종료
    기본 상태는 대기이며 유저는 1개의 대기만 가질 수 있다.
    """

    WAITING = auto()
    ATTENDING = auto()
    IN_PROGRESS = auto()
    TERMINATED = auto()


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
