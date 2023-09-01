import re
from pathlib import Path
from pprint import pformat

from discord.ext import commands

from settings import *
from database import db
from util.console import console


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
        await db.init()
        console.log("Database initialized")
        
        await self.change_presence(activity=DISCORD_PRESENCE)
        console.log(f"logged in as {self.user}")

    async def on_application_command(self, ctx: discord.ApplicationContext) -> None:
        console.log(f"{ctx.author} executed: /{ctx.command}", details=f"Context:\n\n{pformat(vars(ctx))}")


def main() -> None:
    # Create the bot instance
    bot = Zoldicss()

    # Run the bot
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()