import discord
from discord.ext import commands
from discord.commands import Option

from utils.constants import EMOJIS
from data.items import BLOCKS, ITEMS

from utils.classes import db, Tags
from utils.misc import xp_to_next_level
from utils.messages import default_embed, warning
from utils.views.LevelMapView import Level, LevelMapView


class Minerar(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Template")
    async def minerar(
        self,
        ctx: discord.ApplicationContext,
        mobile_support: Option(
            bool,
            name="suporte",
            description="Suporte para celulares",
        ) = False,
    ) -> None:

        WIDTH, HEIGHT = (12, 13) if mobile_support else (13, 13)
        MINING_BLOCKS = [block for block in BLOCKS.values() if "mining" in block.tags]

        with db.modify(ctx.author.id) as player:

            if (player.equiped is None) or (Tags.PICKAXE not in player.equiped.tags):
                await warning(
                    ctx, "Você não tem uma picareta equipada!", ephemeral=True
                )
                return

            level = LevelMapView.create_map(
                blocks=MINING_BLOCKS, player=player, width=WIDTH, height=HEIGHT
            )

            # Create a message to show the map
            def mining_embed(level: Level) -> discord.Embed:
                embed = default_embed(
                    ctx.author,
                    title=f"⛏️ Mineração",
                    description=str(level),
                )

                # Add the player's stats
                embed.add_field(
                    name="**Status:**",
                    value=(
                        f"💰 **Saldo:** ${player.balance:.2f}\n"
                        + f"❤️ **Vida:** {player.health}\n"
                        + f"🍗 **Fome:** {player.hunger}\n"
                        + f"{EMOJIS['xp']} **Experiência:** {player.xp} / {xp_to_next_level(player.level)}"
                    ),
                    inline=True,
                )

                # Add the player's collected items
                embed.add_field(
                    name="**Itens coletados:**",
                    value="\n".join(
                        f"{amount} {ITEMS[item]}"
                        for item, amount in level.player.collected.items()
                    )
                    or "Nenhum",
                    inline=True,
                )

                return embed

            view = LevelMapView.new(ctx, level, mining_embed)

            # Send the message
            await ctx.respond(embed=mining_embed(level), view=view)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Minerar(bot))
