import discord
from discord.ext import commands
from discord.commands import Option
from discord.commands.core import SlashCommand

from utils.messages import default_embed, warning

from utils.consts.images import COMMAND_BLOCK


class Ajuda(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Mostra todos os comandos do bot.")
    async def ajuda(
        self,
        ctx: discord.ApplicationContext,
        command_name: Option(str, name="comando", description="Comando") = None,
    ) -> None:
        def command_to_str(command: commands.Command) -> str:
            # Get all the command options
            arguments = " ".join(
                f"<{'?' if not argument.required else ''}{argument.name}>"
                for argument in command.options
            )

            # Add an whitespace if there are arguments
            arguments = f" {arguments}" if arguments else ""

            return "/" + command.name + arguments

        if command_name:
            command = self.bot.get_application_command(command_name)

            if not command:
                await warning(ctx, "Comando não encontrado.")
                return

            embed = default_embed(
                ctx.author,
                title=f"**Comando: /{command.name}**",
                description=command.description
                + f"\n\nUso: `{command_to_str(command)}`",
            )
            embed.set_thumbnail(url=COMMAND_BLOCK)

            await ctx.respond(embed=embed)
            return

        embed = default_embed(
            ctx.author,
            title="Lista de comandos",
            description="**Utilize `/ajuda <comando>` para mais informações**",
        )

        embed.set_thumbnail(url=COMMAND_BLOCK)
        embed.set_footer(text="Bot criado por: ItaloDoArbusto#4607")

        commands_list = list(self.bot.all_commands.values())
        commands_list.sort(key=lambda command: command.name)

        # Add the commands to the embed
        for command in commands_list:

            # Only show the slash commands
            if not isinstance(command, SlashCommand):
                continue

            # Add the command to the embed
            embed.add_field(
                name=f"`{command_to_str(command)}`",
                value=command.description or "Sem descrição.",
                inline=False,
            )

        # Send the embed
        await ctx.respond(embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Ajuda(bot))
