import discord
from discord.ext import commands

from data.items import BLOCKS, TOOLS

from utils.classes import db
from utils.messages import default_embed, warning
from utils.views.LevelMapView import Level, LevelMapView


class Minerar(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Template")
    async def minerar(self, ctx: discord.ApplicationContext) -> None:
        WIDTH, HEIGHT = 12, 14
        MINING_BLOCKS = [block for block in BLOCKS.values() if "mining" in block.tags]

        with db.modify(ctx.author.id) as player:

            equiped_tool = TOOLS[player.equiped] if player.equiped else None

            if equiped_tool is None or "pickaxe" not in equiped_tool.tags:
                await warning(ctx, "Você não tem uma picareta equipada!")

            level = LevelMapView.create_map(
                blocks=MINING_BLOCKS, player=player, width=WIDTH, height=HEIGHT
            )

            # Create a message to show the map
            def mining_embed(level: Level) -> discord.Embed:
                embed = default_embed(
                    ctx.author,
                    width=34,
                    title=f"⛏️ Mineração",
                    description=str(level),
                )
                return embed
            
            view = LevelMapView.new(ctx, level, mining_embed)

            # Send the message
            await ctx.respond(embed=mining_embed(level), view=view)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Minerar(bot))
