import discord
from discord.ext import commands
from discord.commands import Option

from utils.classes import db
from utils.messages import default_embed
from utils.misc import xp_bar, xp_to_next_level

from utils.constants.emojis import EMOJIS


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.user_command(name="Ver Informações")
    async def _info(self, ctx, user) -> None:
        await self.info(ctx, user)

    @commands.slash_command(description="Mostra seus dados ou os de outro usuario")
    async def info(
        self,
        ctx: discord.ApplicationContext,
        target: Option(discord.Member, name="usuário", description="Usuário") = None,
    ) -> None:

        user = target or ctx.author

        with db.modify(user.id) as player:
            embed = default_embed(user, title="Infomações do Jogador:")

            embed.add_field(
                name="**Combate:**",
                value=(
                    f"{EMOJIS['xp']} **Experiência:** {player.xp} / {xp_to_next_level(player.level)}\n"
                    + f"⚔️ **Ataque:** {player.damage}\n"
                    + f"🛡️ **Defesa:** {player.defense}"
                ),
                inline=True,
            )

            embed.add_field(
                name="**Status:**",
                value=(
                    f"💰 **Saldo:** ${player.balance:.2f}\n"
                    + f"❤️ **Vida:** {player.health}\n"
                    + f"🍗 **Fome:** {player.hunger}"
                ),
                inline=True,
            )

            xp_img = discord.File(
                xp_bar(player.xp / 1000, player.level),
                filename=f"xp_bar.png",
            )
            embed.set_image(url=f"attachment://xp_bar.png")

            await ctx.respond(file=xp_img, embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Info(bot))
