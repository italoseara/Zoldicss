import discord
from discord.ext import commands
from discord.commands import Option

from utils.views import PagesView
from utils.classes import db, MutableInt
from utils.messages import default_embed, warning

from data.items import ITEMS


class Comercio(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Mostra a loja do bot.")
    async def comercio(
        self,
        ctx: discord.ApplicationContext,
        page: Option(int, name="página", description="Página") = 1,
    ) -> None:
        page = MutableInt(page)

        PAGE_SIZE = 5
        pages = [
            list(ITEMS.values())[i : i + PAGE_SIZE]
            for i in range(0, len(list(ITEMS.values())), PAGE_SIZE)
        ]

        if 1 > page > len(pages):
            await warning(ctx, "Página inválida.", ephemeral=True)
            return

        def shop_embed(page: int) -> discord.Embed:
            embed = default_embed(ctx.author, title="Comércio do Zoldicss")

            for item in pages[page - 1]:
                selling = f"${item.selling:.2f}" if item.selling else "Indisponível"
                buying = f"${item.buying:.2f}" if item.buying else "Indisponível"

                embed.add_field(
                    name=str(item),
                    value=f"**Comprar**: {buying}\n**Vender**: {selling}\n`{item.id}`",
                    inline=False,
                )

            embed.set_footer(text=f"Página {page} de {len(pages)}")

            return embed

        pages_view = PagesView.new(
            page=page,
            pages=pages,
            page_embed=shop_embed,
        )

        await ctx.respond(embed=shop_embed(page), view=pages_view)

    @commands.slash_command(description="Comprar um item no comércio.")
    async def comprar(
        self,
        ctx: discord.ApplicationContext,
        item: Option(str, name="item", description="Item"),
        amount: Option(int, name="quantidade", description="Quantidade") = 1,
    ) -> None:

        if item not in ITEMS:
            await warning(ctx, "Item inválido.", ephemeral=True)
            return

        if amount <= 0:
            await warning(ctx, "Quantidade inválida.", ephemeral=True)
            return

        item = ITEMS[item]

        if not item.buying:
            await warning(ctx, "Este item não pode ser comprado.", ephemeral=True)
            return

        with db.modify(ctx.author.id) as player:
            if player.balance < (item.buying * amount):
                await warning(ctx, "Você não tem dinheiro suficiente.", ephemeral=True)
                return

            player.balance -= item.buying * amount
            player.inventory.add(item.id, amount)

        await ctx.respond(
            embed=default_embed(
                ctx.author,
                title="Comércio do Zoldicss",
                description=f"Você comprou {amount}x **{item}** por **${item.buying * amount:.2f}**.",
            )
        )

    @commands.slash_command(description="Vender um item para o comércio.")
    async def vender(
        self,
        ctx: discord.ApplicationContext,
        item: Option(str, name="item", description="Item"),
        amount: Option(int, name="quantidade", description="Quantidade") = 1,
    ) -> None:

        if item not in ITEMS:
            await warning(ctx, "Item inválido.", ephemeral=True)
            return

        if amount <= 0:
            await warning(ctx, "Quantidade inválida.", ephemeral=True)
            return

        item = ITEMS[item]

        if not item.selling:
            await warning(ctx, "Este item não pode ser vendido.", ephemeral=True)
            return

        with db.modify(ctx.author.id) as player:
            if item.id not in player.inventory:
                await warning(ctx, "Você não possui este item.", ephemeral=True)
                return

            if player.inventory[item.id] < amount:
                await warning(
                    ctx, "Você não possui esta quantidade deste item.", ephemeral=True
                )
                return

            player.balance += item.selling * amount
            player.inventory.remove(item.id, amount)

        await ctx.respond(
            embed=default_embed(
                ctx.author,
                title="Comércio do Zoldicss",
                description=f"Você vendeu {amount}x **{item}** por **${item.selling * amount:.2f}**.",
            )
        )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Comercio(bot))
