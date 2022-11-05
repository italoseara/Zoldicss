import random

import discord
from typing import List, Tuple, Any
from dataclasses import dataclass, field

from . import Ore, Tool, MiningLevel


@dataclass
class Block:
    emoji: discord.Emoji
    chance: float  # 0 to 100

    drop: Ore = None
    mining_level: int = MiningLevel.ANY
    tags: List[str] = field(default_factory=list)
    _xp: Tuple[int, int] = field(default_factory=lambda: (0, 0))

    @property
    def xp(self) -> int:
        return random.randint(*self._xp)

    @property
    def hunger(self) -> int:
        return random.randint(1, 5)

    def breakable(self, pickaxe: Tool) -> bool:
        return pickaxe.mining_level >= self.mining_level

    def break_(self, player: Any) -> None:
        # Add the xp to the player's profile
        player.profile.add_xp(self.xp)

        # Add the hunger to the player's profile
        player.profile.hunger.add(self.hunger)
        
        # Add the drop to the player's inventory
        if self.drop and self.breakable(player.tool):
            player.collected.add(self.drop.id)
            player.profile.inventory.add(self.drop.id)
