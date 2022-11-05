from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from utils.constants import EMOJIS

from . import Player
from .constants import MiningLevel


@dataclass
class Item:
    id: str
    name: str
    emoji: str
    selling: Optional[float] = None
    buying: Optional[float] = None
    tags: List[str] = field(default_factory=list)
    crafting: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"{self.emoji} {self.name}"

    def description(self, amount: int = 1) -> str:
        return ""

    def raw_description(self, amount: int = 1) -> str:
        return ""

    def use(self, player: Player, amount: int = 1) -> bool:
        return False

    def partial_emoji(self) -> str:
        if not ":" in self.emoji:
            return self.emoji

        return EMOJIS[self.emoji.replace(":", "")]

    @staticmethod
    def attr_formatter(value, name, emoji, prefix="") -> str:
        f_value = f"{'+' if value > 0 else ''}{prefix}{value:.2f}"
        return f"{emoji} **{name}**: {f_value}" if value != 0 else ""

    @staticmethod
    def raw_attr_formatter(value, name, prefix="") -> str:
        f_value = f"{'+' if value > 0 else ''}{prefix}{value:.2f}"
        return f"{f_value} {name}" if value != 0 else ""


@dataclass
class Economy(Item):
    add_bank: float = 0.0
    add_wallet: float = 0.0

    def description(self, amount: int = 1) -> str:
        attrs = [
            self.attr_formatter(
                value=self.add_bank * amount,
                name="Saldo no banco",
                emoji="🏦",
                prefix="$",
            ),
            self.attr_formatter(
                value=self.add_wallet * amount,
                name="Saldo na carteira",
                emoji="🪙",
                prefix="$",
            ),
        ]

        return "\n".join([attr for attr in attrs if attr])

    def raw_description(self, amount: int = 1) -> str:
        attrs = [
            self.raw_attr_formatter(
                value=self.add_bank * amount, name="Saldo no banco", prefix="$"
            ),
            self.raw_attr_formatter(
                value=self.add_wallet * amount, name="Saldo na carteira", prefix="$"
            ),
        ]

        return "\n".join([attr for attr in attrs if attr])

    def use(self, player: Player, amount: int = 1) -> bool:
        match self.id:
            case "banco":
                # Cannot create more than 1 bank account
                if player.bank.max:
                    return False

                amount = 1

            case "cartao":
                # Cannot use credit card if you don't have a bank account
                if not player.bank.max:
                    return False

        player.bank.max += self.add_bank * amount
        player.balance += self.add_wallet * amount
        return True


@dataclass
class Consumable(Item):
    name: str
    saturation: float = 0.0
    regeneration: float = 0.0

    def description(self, amount: int = 1) -> str:
        attrs = [
            self.attr_formatter(
                value=self.saturation * amount, name="Saturação", emoji="🍗"
            ),
            self.attr_formatter(
                value=self.regeneration * amount, name="Regeneração", emoji="❤️"
            ),
        ]

        return "\n".join([attr for attr in attrs if attr])

    def raw_description(self, amount: int = 1) -> str:
        attr = [
            self.raw_attr_formatter(value=self.saturation * amount, name="Saturação"),
            self.raw_attr_formatter(
                value=self.regeneration * amount, name="Regeneração"
            ),
        ]

        return "\n".join([attr for attr in attr if attr])

    def use(self, player: Player, amount: int = 1) -> bool:
        player.eat(self.saturation * amount)
        player.heal(self.regeneration * amount)
        return True


@dataclass
class Tool(Item):
    durability: float = 0.0
    mining_level: int = MiningLevel.ANY

    def __str__(self) -> str:
        return f"{self.emoji} {self.name} ({self.durability})"

    def _escription(self, amount: int = 1) -> str:
        attrs = [
            self.attr_formatter(
                value=self.durability * amount, name="Durabilidade", emoji="🔩"
            ),
        ]

        return "\n".join([attr for attr in attrs if attr])

    def use(self, player: Player, amount: int = 1) -> bool:
        return True


@dataclass
class Boss(Item):
    # TODO: Give the player a buff
    ...


@dataclass
class Ore(Item):
    ...
