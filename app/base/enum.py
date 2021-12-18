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
        return [enum.name.lower() for enum in cls]

    @classmethod
    def has_value(cls, value) -> bool:
        if value.upper() in cls.get_names():
            print("app 내에서의 enum 사용은 무조건 lower case 입니다")
            return True
        return value in cls.get_names()
