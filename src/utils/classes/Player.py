from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import discord
from dataclasses_json import dataclass_json

from utils.messages import warning

from ._helper import *


@dataclass
class Death:
    MURDER = "murder"
    SUICIDE = "suicide"
    ACCIDENT = "accident"
    STARVATION = "starvation"


@dataclass_json
@dataclass
class Player:
    # Discord
    id: int

    # Player stats
    level: int = 1
    experience: int = 0

    health: Stats = field(default_factory=Stats)
    hunger: Stats = field(default_factory=Stats)

    # Battle
    damage: BattleStats = field(default_factory=BattleStats)
    defense: BattleStats = field(default_factory=BattleStats)

    # Inventory
    inventory: Inventory = field(default_factory=Inventory)

    # Currency
    balance: float = 0.0
    bank: Bank = field(default_factory=dict)

    # Booleans
    inBattle: bool = False

    def user(self, ctx: discord.ApplicationContext) -> discord.User | None:
        return ctx.bot.get_user(self.id)

    async def attack(self, target: Any) -> None:
        # TODO:
        pass

    async def hurt(
        self, ctx: discord.ApplicationContext, amount: int, by: Optional[Any] = None
    ) -> None:
        self.health.current -= amount

        if self.health.current <= 0:
            self.health.current = 0

            if by is not None:
                await self.die(ctx, Death.MURDER, by=by)
                return

            await self.die(ctx, Death.ACCIDENT)

    def heal(self, amount: int) -> None:
        self.health.current += amount
        self.health.current = min(self.health.current, self.health.max)

    def eat(self, amount: int) -> None:
        self.hunger.current += amount
        self.hunger.current = min(self.hunger.current, self.hunger.max)

    async def die(
        self, ctx: discord.ApplicationContext, cause: str, by: Optional[Any] = None
    ) -> None:

        victm = self.user(ctx)

        # Death messages
        match cause:
            case Death.MURDER:
                message = f"{victm.name} foi morto por {by.name}"
            case Death.SUICIDE:
                message = f"{victm.name} se matou"
            case Death.ACCIDENT:
                message = f"{victm.name} morreu por acidente"
            case _:
                message = f"{victm.name} morreu"

        await warning(ctx, message, user=victm)

        # Resets the player
        new = Player(self.id, bank=self.bank)
        self.__dict__ = new.__dict__
