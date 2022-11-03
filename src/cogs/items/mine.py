import discord
from discord.ext import commands

from data.items import BLOCKS


class Minerar(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Template")
    async def minerar(self, ctx: discord.ApplicationContext) -> None:
        await ctx.respond("Ainda não implementado.")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Minerar(bot))
