from enum import Enum
from typing import List


class BaseEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def get_names(cls) -> List:
        return [enum.name for enum in cls]
