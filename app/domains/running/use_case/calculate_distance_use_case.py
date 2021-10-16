from haversine import haversine

from app.domains.running.dto import CalcDistanceData


class CalculateDistanceUseCase:
    def __init__(self):
        pass

    def execute(self, dto: CalcDistanceData) -> int:
        calc_distance = int(haversine(dto.from_data, dto.to_data, unit="m"))
        return calc_distance + dto.distance
