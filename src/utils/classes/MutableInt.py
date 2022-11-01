from dataclasses import dataclass


@dataclass
class MutableInt:
    value: int

    def __int__(self) -> int:
        return self.value

    def __index__(self) -> int:
        return int(self)

    def __add__(self, other: int) -> int:
        return self.value + other

    def __sub__(self, other: int) -> int:
        return self.value - other

    def __mul__(self, other: int) -> int:
        return self.value * other

    def __eq__(self, other: int) -> bool:
        return self.value == other

    def __gt__(self, other: int) -> bool:
        return self.value > other

    def __ge__(self, other: int) -> bool:
        return self.value >= other

    def __lt__(self, other: int) -> bool:
        return self.value < other

    def __le__(self, other: int) -> bool:
        return self.value <= other

    def __repr__(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def __iadd__(self, other: int) -> int:
        self.value += other
        return self.value

    def __isub__(self, other: int) -> int:
        self.value -= other
        return self.value
