from app.domains.running.dto import CalcDistanceData
from app.domains.running.use_case.calculate_distance_use_case import CalculateDistanceUseCase


round_data = [
    (37.355422, 126.936847),
    (37.355435, 126.936721),
    (37.355435, 126.936539),
    (37.355350, 126.936346),
    (37.355235, 126.936207),
    (37.355116, 126.936127),
    (37.354971, 126.935993),
    (37.354805, 126.935867),
    (37.354688, 126.935770),
    (37.354581, 126.935690),
    (37.354481, 126.935634),
    (37.354406, 126.935623),
    (37.354310, 126.935626),
    (37.354229, 126.935656),
    (37.354088, 126.935731),
]


def test_round_running_gps_should_return_expected():
    expected = 180
    distance = 0
    uc = CalculateDistanceUseCase()
    for index, to_data in enumerate(round_data[1:]):
        from_data = round_data[index]
        dto = CalcDistanceData(from_data=from_data, to_data=to_data, distance=distance)
        calc_data = uc.execute(dto)
        distance = calc_data

    assert distance >= expected


def test_calc_same_gps_should_return():
    from_data = (37.354229, 126.935656)
    dto = CalcDistanceData(from_data, from_data)
    uc = CalculateDistanceUseCase()
    res = uc.execute(dto)
    assert res == 0.0
