import discord
from discord.commands import Option
from discord.ext import commands

from utils.classes import db
from utils.messages import default_embed, select_amount, warning

from data.items import ITEMS


class Use(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Usar um item do inventário.")
    async def usar(
        self,
        ctx: discord.ApplicationContext,
        item_id: Option(str, name="id", description="ID do item que será usado."),
        amount: Option(
            int, name="quantidade", description="Quantidade a ser usada."
        ) = None,
    ) -> None:

        with db.modify(ctx.author.id) as player:
            await ctx.response.defer()

            # Check if the item exists
            if not item_id in ITEMS:
                await warning(ctx, "Item não encontrado!", ephemeral=True)
                return

            # Check if the item is not in the inventory
            if not player.inventory[item_id]:
                await warning(ctx, "Você não possui esse item.", ephemeral=True)
                return

            # Select item class
            item = ITEMS[item_id]

            # Check if amount is not specified, then asks for it
            if amount is None:
                amount = await select_amount(
                    self.bot,
                    ctx,
                    message=f"Selecione ou digite a quantidade de {item}:",
                    max_value=player.inventory[item_id],
                    min_value=1,
                )

            # Check if the amount is greater than the player's inventory or less than 1
            if amount < 1 and amount < player.inventory[item_id]:
                await warning(ctx, "Quantidade inválida.", ephemeral=True)
                return

            # Use item
            consumable = item.use(player=player, amount=amount)

            # Item is not usable
            if not consumable:
                await warning(ctx, f"Você não pode usar {item}.", ephemeral=True)
                return

            # Remove item from inventory
            player.inventory.remove(item.id, amount)

            # Send sucess message
            embed = default_embed(
                ctx.author,
                title=f"Você usou {amount}x {item}",
                description=item.description(amount),
            )
            await ctx.respond(embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Use(bot))
