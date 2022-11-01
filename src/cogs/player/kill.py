import discord
from discord.commands import Option
from discord.ext import commands

from utils.messages import warning
from utils.classes import db, Death

from data.admin import ADMINS


class Kill(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.user_command(name="Matar Jogador")
    async def _kill(self, ctx, user) -> None:
        await self.kill(ctx, user)

    @commands.slash_command(description="Se matar, ou matar outro usuário.")
    async def kill(
        self,
        ctx: discord.ApplicationContext,
        target: Option(discord.Member, name="usuário", description="Usuário") = None,
    ) -> None:

        if user and (ctx.author.id not in ADMINS):
            await warning(ctx, "Você não tem permissão para isso!", ephemeral=True)
            return

        user = target or ctx.author

        if user.id not in db.players:
            await warning(ctx, "Este usuário não possui um perfil.", ephemeral=True)
            return

        with db.modify(user.id) as player:
            await player.die(
                ctx=ctx,
                cause=Death.SUICIDE if user == ctx.author else Death.MURDER,
                by=None if user is None else ctx.author,
            )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Kill(bot))
