import random
from typing import Self, Callable
from dataclasses import dataclass

import discord
from discord import ButtonStyle
from discord.ui import View, Button, button

from data.items import TOOLS, BLOCKS
from utils.classes import Block, Player, Tool


@dataclass
class LevelPlayer:
    x: int
    y: int
    tool: Tool


@dataclass
class Level:
    width: int
    height: int

    player: LevelPlayer = None
    map_: list = None

    def move(self, x: int, y: int) -> None:
        if (
            (self.player.x + x >= self.width)
            or (self.player.y + y >= self.height)
            or (self.player.x + x < 0)
            or (self.player.y + y < 0)
        ):
            return

        self.map_[self.player.y][self.player.x] = BLOCKS["background"]
        self.player.x += x
        self.player.y += y
        self.map_[self.player.y][self.player.x] = self.player

    def __str__(self) -> str:
        return "\n".join(
            "".join(
                str(block.emoji)
                if block != self.player
                else str(self.player.tool.emoji)
                for block in row
            )
            for row in self.map_
        )


class LevelMapView(View):
    def __init__(self, level: Level, level_embed: Callable) -> None:
        super().__init__()

        self.level = level
        self.level_embed = level_embed

    @button(
        emoji="⬅️",
        style=ButtonStyle.grey,
        custom_id="move__left",
    )
    async def move_left(self, button: Button, interaction: discord.Interaction) -> None:
        self.level.move(-1, 0)

        await interaction.response.edit_message(
            embed=self.level_embed(self.level), view=self
        )

    @button(
        emoji="⬆️",
        style=ButtonStyle.grey,
        custom_id="move__up",
    )
    async def move_up(self, button: Button, interaction: discord.Interaction) -> None:
        self.level.move(0, -1)

        await interaction.response.edit_message(
            embed=self.level_embed(self.level), view=self
        )

    @button(
        emoji="⬇️",
        style=ButtonStyle.grey,
        custom_id="move__down",
    )
    async def move_down(self, button: Button, interaction: discord.Interaction) -> None:
        self.level.move(0, 1)

        await interaction.response.edit_message(
            embed=self.level_embed(self.level), view=self
        )

    @button(
        emoji="➡️",
        style=ButtonStyle.grey,
        custom_id="move__right",
    )
    async def move_right(
        self, button: Button, interaction: discord.Interaction
    ) -> None:
        self.level.move(1, 0)

        await interaction.response.edit_message(
            embed=self.level_embed(self.level), view=self
        )

    @button(
        emoji="❌",
        style=ButtonStyle.grey,
        custom_id="close",
    )
    async def close(self, button: Button, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message(view=None)

    @classmethod
    def new(cls, level: Level, level_embed: Callable) -> Self | None:
        return cls(level, level_embed) if level.player.tool else None

    @staticmethod
    def create_map(blocks: Block, player: Player, width: int, height: int) -> Level:
        # Create the level
        level = Level(width=width, height=height)

        # Create the player
        level.player = LevelPlayer(
            x=random.randint(0, width - 1),
            y=random.randint(0, height - 1),
            tool=TOOLS[player.equiped],
        )

        # Generate a random map using the chance of each block
        level.map_ = [
            [
                random.choices(blocks, [block.chance for block in blocks])[0]
                for _ in range(width)
            ]
            for _ in range(height)
        ]

        # Put the player in the middle of the map
        level.map_[level.player.y][level.player.x] = level.player

        return level
