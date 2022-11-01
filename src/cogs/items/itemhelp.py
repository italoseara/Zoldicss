import discord
from discord.ext import commands
from discord.commands import Option

from utils.messages import default_embed, warning

from data.items import ITEMS


class AjudaItem(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Mostra as informações de um item.")
    async def ajudaitem(
        self,
        ctx: discord.ApplicationContext,
        item_id: Option(str, name="item", description="ID do item a ser pesquisado"),
    ) -> None:
        if item_id not in ITEMS:
            await warning(ctx, "Este item não existe.", ephemeral=True)
            return

        item = ITEMS[item_id]

        embed = default_embed(
            ctx.author,
            title=f"Informações sobre  {item}",
            description=(
                f"\
                {item.description()}\n\n\
                🪙 **Valor de Compra**: {f'${item.buying:.2f}' if item.buying else 'Indisponível'}\n\
                🪙 **Valor de Venda**: {f'${item.selling:.2f}' if item.selling else 'Indisponível'}\
            "
            ),
        )
        embed.set_footer(text=f"ID: {item_id}")

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(AjudaItem(bot))
