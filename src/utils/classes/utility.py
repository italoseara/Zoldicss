from dataclasses import dataclass


@dataclass
class Vector:
    x: int
    y: int

    def inside(self, other: "Vector") -> bool:
        return (
            (self.x >= 0)
            and (self.y >= 0)
            and (self.x < other.x)
            and (self.y < other.y)
        )


@dataclass
class Stats:
    current: int = 100
    max: int = 100

    def __str__(self) -> str:
        return f"{self.current} / {self.max}"

    def add(self, amount: int) -> None:
        self.current -= amount

        if self.current < 0:
            self.current = 0

@dataclass
class BattleStats:
    min: int = 0
    max: int = 0

    def __str__(self) -> str:
        return f"{self.min} ➜ {self.max}"


@dataclass
class Bank:
    balance: float = 0.0
    max: float = 0.0

    def __str__(self) -> str:
        return f"${self.balance:.2f} / ${self.max:.2f}"


class Inventory(dict):
    def __str__(self) -> str:
        return ", ".join(f"{item} x{count}" for item, count in self.__dict__.items())

    def __getitem__(self, key) -> int:
        return self.__dict__[key] if key in self.__dict__ else 0

    def __repr__(self) -> str:
        return repr(self.__dict__)

    def items(self) -> list[tuple[str, int]]:
        return list(self.__dict__.items())

    def add(self, item: str, amount: int = 1) -> None:
        if item in self.__dict__:
            self.__dict__[item] += amount
        else:
            self.__dict__[item] = amount

    def remove(self, item: str, amount: int) -> None:
        if item in self.__dict__:
            self.__dict__[item] -= amount
            if self.__dict__[item] <= 0:
                del self.__dict__[item]
