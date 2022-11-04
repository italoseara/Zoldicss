import discord
from discord.ext import commands
from discord.commands import Option

from utils.views import PagesView
from utils.classes import db, MutableInt
from utils.messages import default_embed, warning

from data.items import ITEMS


class Inventario(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.user_command(name="Ver Inventário")
    async def _inventario(self, ctx, user) -> None:
        await self.inventario(ctx, user)

    @commands.slash_command(description="Mostra o inventário do jogador.")
    async def inventario(
        self,
        ctx: discord.ApplicationContext,
        target: Option(discord.Member, name="usuário", description="Usuário") = None,
        page: Option(int, name="página", description="Página") = 1,
    ) -> None:

        user = target or ctx.author
        page = MutableInt(page)

        if user.id not in db.players:
            await warning(ctx, "Este usuário não possui um perfil.", ephemeral=True)
            return

        with db.modify(user.id) as player:
            # Setup the inventory pages
            PAGE_SIZE = 4
            pages = [
                player.inventory.items()[i : i + PAGE_SIZE]
                for i in range(0, len(player.inventory.items()), PAGE_SIZE)
            ]

            if 1 > page > len(pages):
                await warning(ctx, "Página inválida.", ephemeral=True)
                return

            # Create the embed
            def inventory_embed(page: int) -> discord.Embed:
                if not pages:
                    return default_embed(
                        user,
                        title="Inventário",
                        description="Inventário vazio.",
                    )

                embed = default_embed(user, title="Inventário")

                for item_id, amount in pages[page - 1]:
                    item = ITEMS[item_id]

                    embed.add_field(
                        name=f"**{item} — {amount}**",
                        value=f"{item.raw_description()}\n`{item.id}`",
                        inline=False,
                    )

                embed.set_footer(text=f"Página {page} de {len(pages)}")

                return embed

            pages_view = PagesView.new(
                ctx=ctx,
                page=page,
                pages=pages,
                page_embed=inventory_embed,
            )

            # Send the message
            await ctx.respond(embed=inventory_embed(page), view=pages_view)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Inventario(bot))
