from pydantic.dataclasses import dataclass


@dataclass
class CalcDistanceDto:
    from_data: tuple = (0, 0)
    to_data: tuple = (0, 0)
    distance: int = 0
