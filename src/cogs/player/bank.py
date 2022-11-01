import discord
from discord.ext import commands
from discord.commands import Option

from utils.classes import db
from utils.messages import default_embed, warning


class Banco(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Verifique seu saldo na conta bancária.")
    async def banco(
        self,
        ctx: discord.ApplicationContext,
        user: Option(
            discord.User, description="Usuário que você deseja verificar o saldo."
        ) = None,
    ) -> None:
        user = user or ctx.author

        if user.id not in db.players:
            await warning(ctx, "Este usuário não possui um perfil.", ephemeral=True)
            return

        with db.modify(user.id) as player:
            embed = default_embed(
                user,
                title="🏦 Banco do Zoldicss",
                description=f"\u2800\n**Saldo atual**: {player.bank}.\n\u2800",
            )
            embed.set_footer(
                text="Use /depositar, /sacar ou /transferir para fazer transações."
            )

            if not player.bank.max:
                embed.set_footer(
                    text="Você ainda não possui um banco."
                    if user == ctx.author
                    else f"{user} ainda não possui um banco."
                )

            await ctx.respond(embed=embed)

    @commands.slash_command(description="Deposite dinheiro na sua conta bancária.")
    async def depositar(
        self,
        ctx: discord.ApplicationContext,
        amount: Option(
            int,
            name="quantidade",
            description="Quantidade de dinheiro a ser depositada.",
        ) = None,
    ) -> None:
        with db.modify(ctx.author.id) as player:
            if amount is None:
                amount = player.balance

            if player.bank.balance + amount > player.bank.max:
                amount = player.bank.max - player.bank.balance

            if amount <= 0:
                await ctx.respond(
                    embed=warning(
                        ctx.author,
                        "Você não pode depositar essa quantidade de dinheiro.",
                    )
                )
                return

            if amount > player.balance:
                await ctx.respond(
                    embed=warning(
                        ctx.author, "Você não possui essa quantidade de dinheiro."
                    )
                )
                return

            player.balance -= amount
            player.bank.balance += amount

            await ctx.respond(
                embed=default_embed(
                    ctx.author,
                    title="🏦 Banco do Zoldicss",
                    description=f"**Depósito realizado**: ${amount:.2f}.",
                )
            )

    @commands.slash_command(description="Saque dinheiro da sua conta bancária.")
    async def sacar(
        self,
        ctx: discord.ApplicationContext,
        amount: Option(
            int, name="quantidade", description="Quantidade de dinheiro a ser sacada"
        ) = None,
    ) -> None:
        with db.modify(ctx.author.id) as player:
            if not player.bank.max:
                await ctx.respond(
                    embed=warning(ctx.author, "Você ainda não possui um banco.")
                )
                return

            if amount is None:
                amount = player.bank.balance

            if amount <= 0:
                await ctx.respond(
                    embed=warning(
                        ctx.author, "Você não pode sacar essa quantidade de dinheiro."
                    )
                )
                return

            if amount > player.bank.balance:
                await ctx.respond(
                    embed=warning(
                        ctx.author,
                        "Você não possui essa quantidade de dinheiro na conta bancária.",
                    )
                )
                return

            player.balance += amount
            player.bank.balance -= amount

            await ctx.respond(
                embed=default_embed(
                    ctx.author,
                    title="🏦 Banco do Zoldicss",
                    description=f"**Saque realizado**: ${amount:.2f}.",
                )
            )

    @commands.slash_command(
        description="Transfira dinheiro da sua conta bancária para outra pessoa."
    )
    async def transferir(
        self,
        ctx: discord.ApplicationContext,
        user: discord.Member,
        amount: Option(
            int,
            name="quantidade",
            description="Quantidade de dinheiro a ser transferida.",
        ),
    ) -> None:
        with db.modify(ctx.author.id) as player:
            with db.modify(user.id) as target:
                if not player.bank.max:
                    await warning(ctx, "Você ainda não possui um banco.")
                    return

                if not target.bank.max:
                    await warning(ctx, "O usuário não possui um banco.")
                    return

                if target.bank.balance + amount > target.bank.max:
                    amount = target.bank.max - target.bank.balance

                if amount <= 0:
                    await warning(
                        ctx.author,
                        "Você não pode transferir essa quantidade de dinheiro.",
                    )
                    return

                if amount > player.bank.balance:
                    await warning(
                        ctx.author,
                        "Você não possui essa quantidade de dinheiro na conta bancária.",
                    )
                    return

                player.bank.balance -= amount
                target.bank.balance += amount

                await ctx.respond(
                    embed=default_embed(
                        ctx.author,
                        title="🏦 Banco do Zoldicss",
                        description=f"**Transferência realizada para {user.mention}**: ${amount:.2f}.",
                    )
                )

    @commands.slash_command(
        description="Mostre o ranking dos 10 jogadores com mais dinheiro."
    )
    async def baltop(self, ctx: discord.ApplicationContext) -> None:

        # Sort players by balance once more
        players = sorted(
            self.bot.baltop, key=lambda player: player.balance, reverse=True
        )

        embed = default_embed(
            ctx.author,
            title="🏦 Banco do Zoldicss",
            description="**Ranking de dinheiro dos 10 jogadores mais ricos**:\n\n",
        )

        for index, player in enumerate(players):
            embed.description += f"**{index + 1}º** {self.bot.get_user(player.id).mention} — ${player.balance:.2f}\n"

        embed.set_footer(text="Ranking atualizado a cada 5 minutos.")

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Banco(bot))
