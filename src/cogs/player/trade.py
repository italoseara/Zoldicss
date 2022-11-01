import asyncio
import discord
from discord import Status
from discord.ext import commands
from discord.commands import Option

from utils.classes import db
from utils.messages import default_embed, warning


class Trocar(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.user_command(name="Propor Troca")
    async def _trocar(self, ctx, user) -> None:
        await self.trocar(ctx, user)

    @commands.slash_command(description="Troca de itens entre jogadores.")
    async def trocar(
        self,
        ctx: discord.ApplicationContext,
        target: Option(discord.Member, name="usuário", description="Usuário"),
    ) -> None:
        from utils.views.TradeView import AuthorView, TargetView, Trade

        if target == ctx.author:
            await warning(ctx, "Você não pode trocar com você mesmo.", ephemeral=True)
            return

        if target.bot:
            await warning(ctx, "Você não pode trocar com um bot.", ephemeral=True)
            return

        if ctx.guild.get_member(target.id).status == Status.offline:
            await warning(ctx, "O usuário está offline.", ephemeral=True)
            return

        if target.id not in db.players:
            await warning(ctx, "Este usuário não possui um perfil.", ephemeral=True)
            return

        trade = Trade()
        trade.bot = self.bot

        with db.modify(ctx.author.id) as trade.author.profile:
            with db.modify(target.id) as trade.target.profile:

                trade.target.user = target
                trade.author.user = ctx.author

                await ctx.respond(
                    embed=default_embed(
                        trade.author.user,
                        title="Proposta de Troca",
                        description=f"Sua proposta de troca foi enviada para {trade.target.user.mention}.",
                    ),
                    ephemeral=True,
                )

                # Create the embeds
                author_embed = default_embed(
                    trade.author.user,
                    title=f"Aguardando resposta de {trade.target.user}...",
                )
                author_embed.add_field(name="\u2800", value=trade.target.user.mention)
                author_embed.set_footer(text="Clique em ❌ para cancelar a troca.")

                target_embed = default_embed(
                    trade.target.user,
                    title=f"Você recebeu uma proposta de troca de {trade.author.user}!",
                )
                target_embed.add_field(name="\u2800", value=trade.author.user.mention)
                target_embed.set_footer(
                    text="Clique em ✅ para aceitar ou ❌ para recusar."
                )

                # Send the messages
                done, _ = await asyncio.wait(
                    [
                        asyncio.create_task(
                            trade.author.user.send(
                                embed=author_embed,
                                view=AuthorView(trade),
                                delete_after=300,
                            )
                        ),
                        asyncio.create_task(
                            trade.target.user.send(
                                embed=target_embed,
                                view=TargetView(trade),
                                delete_after=300,
                            )
                        ),
                    ],
                    return_when=asyncio.ALL_COMPLETED,
                )

                # Set trade.author.message and trade.target.message
                for future in done:
                    if future.result().channel.recipient == trade.author.user:
                        trade.author.interaction = future.result()
                    else:
                        trade.target.interaction = future.result()

                # Wait for trade to be finished
                await trade.wait()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Trocar(bot))
