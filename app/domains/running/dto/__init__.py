from pydantic.dataclasses import dataclass


@dataclass
class CalcDistanceData:
    from_data: tuple = (0, 0)
    to_data: tuple = (0, 0)
    distance: int = 0


@dataclass
class CreateRoomData:
    user_id: str = ""
    category: str = ""
    mode: str = ""
    config: dict = None
