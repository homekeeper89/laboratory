from typing import List
from app.base.base_enum import BaseEnum
from enum import auto


class RunningParticipantEnum(BaseEnum):
    """
    running 참가자들의 상태
    대기 > 진행 > 일시정지 > (중도 이탈, 완주)
    """

    WAITING = auto()
    IN_PROGRESS = auto()
    PAUSE = auto()
    DROP_OUT = auto()
    FINISH = auto()


class RunningStatusEnum(BaseEnum):
    """
    running 의 상태,
    참가 > 진행 > 종료
    기본 상태는 대기이며 유저는 1개의 대기만 가질 수 있다.
    """

    ATTENDING = auto()
    IN_PROGRESS = auto()
    TERMINATED = auto()

    @classmethod
    def get_invalid_status(cls) -> List:
        return [cls.IN_PROGRESS, cls.ATTENDING]


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
