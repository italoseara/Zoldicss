import discord
from typing import List
from dataclasses import dataclass, field

from . import Ore, Tool, MiningLevel


@dataclass
class Block:
    emoji: discord.Emoji
    chance: float  # 0 to 1
    drop: Ore = None
    mining_level: int = MiningLevel.ANY
    tags: List[str] = field(default_factory=list)

    def break_(self, pickaxe: Tool) -> bool:
        return pickaxe.mining_level >= self.mining_level
