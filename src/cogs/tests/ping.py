from random import choice

import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Teste de ping.")
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        phrases = [
            "tudo certo patrao :thumbsup:",
            "pau no gato :thumbsup:",
            "dale :thumbsup:",
            "po fica safe, ta td certo :thumbsup:",
            "o melhor da bahia, graças a deus :thumbsup:",
        ]

        await ctx.respond(f"{choice(phrases)} `{round(self.bot.latency * 1000)}ms`")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Ping(bot))
