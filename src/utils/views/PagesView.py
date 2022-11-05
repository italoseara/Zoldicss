from typing import Self, List, Any, Callable

import discord
from discord import ButtonStyle
from discord.ui import View, Button, button


class PagesView(View):
    def __init__(
        self,
        ctx: discord.ApplicationContext,
        page: int,
        pages: List[List[Any]],
        page_embed: Callable,
    ) -> None:
        super().__init__()

        self.ctx = ctx
        self.page = page
        self.pages = pages
        self.page_embed = page_embed

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author

    @button(
        emoji="⬅️",
        style=ButtonStyle.grey,
        custom_id="previous",
    )
    async def previous_page(
        self, button: Button, interaction: discord.Interaction
    ) -> None:
        self.page -= 1
        self.children[0].disabled = self.page == 1
        self.children[1].disabled = self.page == len(self.pages)

        await interaction.response.edit_message(
            embed=self.page_embed(self.page), view=self
        )

    @button(
        emoji="➡️",
        style=ButtonStyle.grey,
        custom_id="next_page",
    )
    async def next_page(self, button: Button, interaction: discord.Interaction) -> None:
        self.page += 1
        self.children[0].disabled = self.page == 1
        self.children[1].disabled = self.page == len(self.pages)

        await interaction.response.edit_message(
            embed=self.page_embed(self.page), view=self
        )

    @button(emoji="❌", style=ButtonStyle.grey, custom_id="close")
    async def close(self, button: Button, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message(delete_after=0)

    @classmethod
    def new(
        cls,
        ctx: discord.ApplicationContext,
        page: int,
        pages: List[List[Any]],
        page_embed: Callable,
    ) -> Self | None:
        view = cls(ctx, page, pages, page_embed)

        view.children[0].disabled = page == 1
        view.children[1].disabled = page == len(pages)

        return view if pages else None
