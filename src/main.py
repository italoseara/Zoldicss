import re
from pathlib import Path
from pprint import pformat
from discord.commands import ApplicationContext
from discord.errors import DiscordException

from discord.ext import commands

from settings import *
from database import User
from util.console import console
from util.autosqlite import session

class Zoldicss(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            intents=DISCORD_INTENTS,
            command_prefix=DISCORD_COMMAND_PREFIX,
            application_id=DISCORD_APPLICATION_ID,
        )

        self.load_cogs()

    def load_cogs(self) -> None:
        # Load all cogs from the cogs directory
        for extension_path in Path("src/cogs").glob("**/*.py"):
            if not extension_path.parts[-1].startswith("_"):
                extension_name = re.sub(r"^(.+)\.py$", r"\1", str.join(".", list(extension_path.parts[1:])))

                console.log(f"Loading cog: {extension_name}")
                self.load_extension(extension_name)

        self.remove_command("help")

    async def on_ready(self) -> None:     
        async with session as s:
            await s.create(User)
            await s.check(User)

            console.log(f"Connected to database: {s.path}")
           
        await self.change_presence(activity=DISCORD_PRESENCE)
        console.log(f"logged in as {self.user}",
                    details=f"User tag: {self.user}\n"
                            f"User ID: {self.user.id}\n"
                            f"Guilds: {', '.join(map(str, self.guilds))}\n")

    async def on_application_command(self, ctx: discord.ApplicationContext) -> None:
        console.log(f"{ctx.author} executed: /{ctx.command}", 
                    details=f"Application Context:\n\n{pformat(vars(ctx))}")

    async def on_application_command_error(self, context: ApplicationContext, exception: DiscordException) -> None:
        console.log(f"Error executing command: /{context.command}", 
                    details=f"Exception:\n\n{pformat(vars(exception))}")


def main() -> None:
    bot = Zoldicss()
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()