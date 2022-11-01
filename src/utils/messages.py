import random
import asyncio
from typing import Any, Optional

import discord
from discord import ButtonStyle
from discord.ext import commands
from discord.ui import View, Button, button

from utils.misc import num_emoji


def random_color() -> int:
    return random.randint(0, 0xFFFFFF)


def default_embed(user: discord.Member, title: str, color: str = None, width: int = 25, **kwargs) -> discord.Embed:
    # Put title in the left of a 30 character wide filled with blank space
    embed = discord.Embed(color=color or random_color(),
                          title=title.ljust(width, "\u2800"), **kwargs)

    embed.set_author(
        name=str(user),
        icon_url=f"{user.display_avatar.url}",
    )

    return embed


def warning(
    ctx: discord.ApplicationContext,
    message: str,
    user: Optional[discord.User] = None,
    **kwargs: Any,
) -> discord.Coroutine:

    user = user or ctx.author

    embed = default_embed(user, title=message)
    return ctx.respond(embed=embed, **kwargs)


async def select_amount(
    bot: commands.Bot,
    ctx: discord.ApplicationContext | discord.Interaction,
    message: str,
    max_value: int = None,
    min_value: int = 1,
) -> int:

    amount = 1

    class AmountView(View):

        @classmethod
        async def update_message(cls, interaction) -> None:
            embed = default_embed(
                ctx.author,
                title=message,
                description=f"Quantidade: {num_emoji(amount)}",
            )
            embed.set_footer(text=f"min: {min_value} ➜ max: {max_value}")

            await interaction.response.edit_message(embed=embed, view=cls())

        @button(style=ButtonStyle.danger, emoji="✖️", custom_id="cancel")
        async def cancel(self, button: Button, interaction: discord.Interaction) -> None:
            await interaction.response.edit_message(
                embed=default_embed(ctx.author, title="Operação cancelada."),
                view=None,
                delete_after=2
            )

        @button(style=ButtonStyle.primary, emoji="➖", custom_id="minus_one")
        async def minus_one(self, button: Button, interaction: discord.Interaction) -> None:
            nonlocal amount

            amount -= 1
            amount = max(amount, min_value)

            await self.update_message(interaction)

        @button(style=ButtonStyle.primary, emoji="➕", custom_id="plus_one")
        async def plus_one(self, button: Button, interaction: discord.Interaction) -> None:
            nonlocal amount

            amount += 1
            amount = min(amount, max_value)

            await self.update_message(interaction)

        @button(style=ButtonStyle.success, emoji="✔️", custom_id="confirm")
        async def confirm(self, button: Button, interaction: discord.Interaction) -> None:
            await interaction.response.defer()

    embed = default_embed(
        ctx.author,
        title=message,
        description=f"Quantidade: {num_emoji(amount)}",
    )
    embed.set_footer(text=f"min: {min_value} ➜ max: {max_value}")

    response = await ctx.send(embed=embed, view=AmountView())

    def button_check(interaction: discord.Interaction) -> bool:
        return (
            interaction.user == ctx.author
            and interaction.message.id == response.id
            and interaction.custom_id == "confirm"
        )

    def message_check(message: discord.Message) -> bool:
        return (
            message.author == ctx.author
            and message.channel.id == ctx.channel.id
            and message.content.isdigit()
            and int(message.content) in range(min_value, max_value + 1)
        )

    done, pending = await asyncio.wait([
        asyncio.create_task(bot.wait_for("interaction", check=button_check)),
        asyncio.create_task(bot.wait_for("message", check=message_check))
    ], return_when=asyncio.FIRST_COMPLETED)

    if done and not isinstance((interaction := done.pop().result()), discord.Interaction):
        amount = int(interaction.content)

    for task in pending:
        task.cancel()

    await response.delete()

    if not ctx.response.is_done():
        await ctx.response.defer()

    return amount
