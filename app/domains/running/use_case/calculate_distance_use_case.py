from haversine import haversine

from app.domains.running.dto import CalcDistanceDto


class CalculateDistanceUseCase:
    def __init__(self):
        pass

    def execute(self, dto: CalcDistanceDto) -> int:
        calc_distance = int(haversine(dto.from_data, dto.to_data, unit="m"))
        return calc_distance + dto.distance
