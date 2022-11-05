import discord
from discord.ext import commands
from discord.commands import Option

from data.items import TOOLS, ITEMS
from utils.messages import default_embed, warning
from utils.classes import db


class Equipar(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Template")
    async def equipar(
        self,
        ctx: discord.ApplicationContext,
        item_id: Option(str, name="id", description="ID do item que será equipado."),
    ) -> None:

        if item_id not in ITEMS:
            await warning(ctx, "Item não encontrado!", ephemeral=True)
            return

        if item_id not in TOOLS:
            await warning(ctx, "Este item não é uma ferramenta!", ephemeral=True)
            return

        with db.modify(ctx.author.id) as player:
            if item_id not in player.inventory:
                await warning(ctx, "Você não possui este item!", ephemeral=True)
                return

            player._equiped = item_id

            await warning(ctx, f"Você equipou {ITEMS[item_id]}")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Equipar(bot))
