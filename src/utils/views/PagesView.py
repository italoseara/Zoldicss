import discord
from discord import ButtonStyle
from discord.ui import View, Button, button


class PagesView(View):

    def __init__(self, page, pages, page_embed) -> None:
        super().__init__()

        self.page = page
        self.pages = pages
        self.page_embed = page_embed

    @button(
        emoji="⬅️",
        style=ButtonStyle.grey,
        custom_id="previous",
    )
    async def previous_page(self, button: Button, interaction: discord.Interaction) -> None:
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
            embed=self.page_embed(self.page),
            view=self
        )

    @button(emoji="❌", style=ButtonStyle.grey, custom_id="close")
    async def close(self, button: Button, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message(view=None)

def create_view(page, pages, page_embed) -> PagesView | None:
    view = PagesView(page, pages, page_embed)

    view.children[0].disabled = page == 1
    view.children[1].disabled = page == len(pages)

    return view if pages else None