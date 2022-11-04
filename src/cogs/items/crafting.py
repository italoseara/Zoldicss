import discord
from discord.ext import commands
from discord.commands import Option

from utils.views import PagesView
from utils.classes import MutableInt, db
from utils.messages import default_embed, warning

from data.items import CRAFTABLES, ITEMS


class Crafting(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Lista todos os itens que podem ser craftados")
    async def craftaveis(
        self,
        ctx: discord.ApplicationCommand,
        page: Option(int, name="página", description="Página") = 1,
    ) -> None:
        page = MutableInt(page)

        PAGE_SIZE = 4
        pages = [
            list(CRAFTABLES.values())[i : i + PAGE_SIZE]
            for i in range(0, len(list(CRAFTABLES.values())), PAGE_SIZE)
        ]

        if 1 > page > len(pages):
            await warning(ctx, "Página inválida.", ephemeral=True)
            return

        def craft_embed(page: int) -> discord.Embed:
            embed = default_embed(
                ctx.author,
                title="Itens craftáveis",
                description="Use `/craftar <item>` com os materiais\n necessários para craftar um item.",
                width=35,
            )

            for item in pages[page - 1]:
                embed.add_field(
                    name=str(item),
                    value="\n".join(
                        [
                            f"- {ITEMS[ingredient].emoji} {ITEMS[ingredient].name} **{amount}x**"
                            for ingredient, amount in item.crafting.items()
                        ]
                    ),
                    inline=False,
                )

            embed.set_footer(text=f"Página {page} de {len(pages)}")

            return embed

        pages_view = PagesView.new(
            ctx=ctx,
            page=page,
            pages=pages,
            page_embed=craft_embed,
        )

        await ctx.respond(embed=craft_embed(page), view=pages_view)

    @commands.slash_command(description="Crafta um item")
    async def craftar(
        self,
        ctx: discord.ApplicationCommand,
        item: Option(str, name="item", description="Item"),
    ) -> None:
        # TODO: Colocar quantidade

        if item not in CRAFTABLES:
            await warning(ctx, "Item inválido.", ephemeral=True)
            return

        item = CRAFTABLES[item]

        with db.modify(ctx.author.id) as player:
            for ingredient, amount in item.crafting.items():
                if (not (ingredient in player.inventory)) or (
                    player.inventory[ingredient] < amount
                ):
                    await warning(
                        ctx,
                        f"Você não possui os materiais necessários para craftar {item}.",
                        ephemeral=True,
                    )
                    return

                player.inventory.remove(ingredient, amount)

            player.inventory.add(item.id)

        await ctx.respond(
            embed=default_embed(
                ctx.author,
                title="Item craftado",
                description=f"Você craftou {item} com sucesso!",
            )
        )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Crafting(bot))
