import discord
from discord.ext import commands


class Template(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Template")
    async def template(self, ctx: discord.ApplicationContext) -> None:
        await ctx.response.defer()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Template(bot))
