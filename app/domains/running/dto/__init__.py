from pydantic.dataclasses import dataclass
from app.domains.running.enum import RunningCategoryEnum, RunningModeEnum


@dataclass
class RunningConfigData:
    """
    distance: meter 기준
    """

    distance: int = 500
    limit_minutes: int = 10
    limit_user_counts: int = 4


@dataclass
class CalcDistanceData:
    from_data: tuple = (0, 0)
    to_data: tuple = (0, 0)
    distance: int = 0


@dataclass
class CreateRunningData:
    user_id: int = 0
    category: RunningCategoryEnum = RunningCategoryEnum.PRIVATE
    mode: RunningModeEnum = RunningModeEnum.COMPETITION
    config: RunningConfigData = RunningConfigData()

    def make(self, **kwargs):
        for key, value in kwargs.items():
            if key == "config":
                for n_key, n_value in value.items():
                    setattr(self.config, n_key, n_value)
                continue
            value = value.upper()
            setattr(self, key, value)
        return self
