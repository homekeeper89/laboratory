from app.domains.running.dto import CalcDistanceData
from app.domains.running.use_case.calculate_distance_use_case import CalculateDistanceUseCase


def test_round_running_gps_should_return_expected(get_round_data):
    expected = 180
    distance = 0
    uc = CalculateDistanceUseCase()
    for index, to_data in enumerate(get_round_data[1:]):
        from_data = get_round_data[index]
        dto = CalcDistanceData(from_data=from_data, to_data=to_data, distance=distance)
        calc_distance = uc.execute(dto)
        distance = calc_distance

    assert distance >= expected


def test_calc_same_gps_should_return():
    from_data = (37.354229, 126.935656)
    dto = CalcDistanceData(from_data, from_data)
    uc = CalculateDistanceUseCase()
    res = uc.execute(dto)
    assert res == 0.0
