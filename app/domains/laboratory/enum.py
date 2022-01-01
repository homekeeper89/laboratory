from enum import Enum, auto


class StrEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        """
        print() 할때 호출 됨
        """
        return self.name


class BasicEnum(Enum):
    HELLO_WORLD = "HELLO_WORLD"


class AdvancedStrEnum(StrEnum):
    HELLO_WORLD = auto()
