import discord
from discord.ext import commands
from database import db

from database import User

class DatabaseTest(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="database", description="Test")
    async def database(self, ctx: discord.ApplicationContext) -> None:
        async with User(db, ctx.author.id, ctx.guild.id) as user:
            user.teste.append(123)
            await ctx.respond(f"XP: {user.xp}\nLevel: {user.level}")

def setup(bot: commands.Bot) -> None:
    bot.add_cog(DatabaseTest(bot))