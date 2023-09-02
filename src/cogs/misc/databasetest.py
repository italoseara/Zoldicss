import discord
from discord.ext import commands

from database import User
from util.autosqlite import session

class DatabaseTest(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="database", description="Test")
    async def database(self, ctx: discord.ApplicationContext) -> None:
        async with session as s:
            user = await s.get(User, id=ctx.author.id, guild=ctx.guild.id)
            user.inventory["test"] = 1

            await s.update(user)
            await ctx.respond(f"User: {user}")

def setup(bot: commands.Bot) -> None:
    bot.add_cog(DatabaseTest(bot))