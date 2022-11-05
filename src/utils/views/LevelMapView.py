import random
from typing import Self, Callable
from dataclasses import dataclass, field

import discord
from discord import ButtonStyle
from discord.ui import View, Button, button

from data.items import TOOLS, BLOCKS
from utils.classes import Block, Player, Tool, Inventory, Vector


@dataclass
class LevelPlayer(Vector):
    tool: Tool
    profile: Player
    collected: Inventory = field(default_factory=Inventory)


@dataclass
class Level:
    width: int
    height: int

    player: LevelPlayer = None
    map_: list = None

    def move(self, x: int, y: int) -> None:
        new_pos = Vector(x=self.player.x + x, y=self.player.y + y)

        if not new_pos.inside(Vector(x=self.width, y=self.height)):
            return

        block = self.map_[new_pos.y][new_pos.x]
        if block.drop and self.player.tool.mining_level >= block.mining_level:
            self.player.collected.add(block.drop.id)
            self.player.profile.inventory.add(block.drop.id)

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
    def __init__(
        self, ctx: discord.ApplicationContext, level: Level, level_embed: Callable
    ) -> None:
        super().__init__()

        self.ctx = ctx
        self.level = level
        self.level_embed = level_embed

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author

    @button(
        label="\u200b",
        style=ButtonStyle.grey,
        row=0,
    )
    async def blank1(self, button: Button, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

    @button(
        emoji="⬆️",
        style=ButtonStyle.grey,
        custom_id="move__up",
        row=0,
    )
    async def move_up(self, button: Button, interaction: discord.Interaction) -> None:
        self.level.move(0, -1)

        await interaction.response.edit_message(
            embed=self.level_embed(self.level), view=self
        )

    @button(
        label="\u200b",
        style=ButtonStyle.grey,
        row=0,
    )
    async def blank2(self, button: Button, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

    @button(
        emoji="⬅️",
        style=ButtonStyle.grey,
        custom_id="move__left",
        row=1,
    )
    async def move_left(self, button: Button, interaction: discord.Interaction) -> None:
        self.level.move(-1, 0)

        await interaction.response.edit_message(
            embed=self.level_embed(self.level), view=self
        )

    @button(
        emoji="❌",
        style=ButtonStyle.grey,
        custom_id="close",
        row=1,
    )
    async def close(self, button: Button, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message(delete_after=0)

    @button(
        emoji="➡️",
        style=ButtonStyle.grey,
        custom_id="move__right",
        row=1,
    )
    async def move_right(
        self, button: Button, interaction: discord.Interaction
    ) -> None:
        self.level.move(1, 0)

        await interaction.response.edit_message(
            embed=self.level_embed(self.level), view=self
        )

    @button(
        label="\u200b",
        style=ButtonStyle.grey,
        row=2,
    )
    async def blank3(self, button: Button, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

    @button(
        emoji="⬇️",
        style=ButtonStyle.grey,
        custom_id="move__down",
        row=2,
    )
    async def move_down(self, button: Button, interaction: discord.Interaction) -> None:
        self.level.move(0, 1)

        await interaction.response.edit_message(
            embed=self.level_embed(self.level), view=self
        )

    @button(
        label="\u200b",
        style=ButtonStyle.grey,
        row=2,
    )
    async def blank4(self, button: Button, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

    @classmethod
    def new(
        cls, ctx: discord.ApplicationContext, level: Level, level_embed: Callable
    ) -> Self | None:
        return cls(ctx, level, level_embed) if level.player.tool else None

    @staticmethod
    def create_map(blocks: Block, player: Player, width: int, height: int) -> Level:
        # Create the level
        level = Level(width=width, height=height)

        # Create the player
        level.player = LevelPlayer(
            x=random.randint(0, width - 1),
            y=random.randint(0, height - 1),
            tool=TOOLS[player.equiped],
            profile=player,
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
