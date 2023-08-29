import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="ping", description="Pong!")
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        await ctx.respond(f"🏓 Pong! `{round(self.bot.latency * 1000)}ms`")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Ping(bot))