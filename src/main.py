import re
from pathlib import Path
from datetime import datetime

from discord.ext import commands

from settings import *
from database import db


class Zoldicss(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            intents=DISCORD_INTENTS,
            command_prefix=DISCORD_COMMAND_PREFIX,
            application_id=DISCORD_APPLICATION_ID,
        )

        self.load_cogs()

    def log(self, message: str) -> None:
        date = datetime.now().strftime("%d-%m-%Y")
        time = datetime.now().strftime("%H:%M:%S")

        print(f"[{time}] - {message}")

        if not Path("logs").exists():
            Path("logs").mkdir()

        with open(f"logs/{date}.log", "a") as log_file:
            log_file.write(f"[{time}] - {message}\n")

    def load_cogs(self) -> None:
        # Load all cogs from the cogs directory
        for extension_path in Path("src/cogs").glob("**/*.py"):
            if not extension_path.parts[-1].startswith("_"):
                extension_name = re.sub(r"^(.+)\.py$", r"\1", str.join(".", list(extension_path.parts[1:])))

                self.log(f"Loading cog: {extension_name}")
                self.load_extension(extension_name)

        self.remove_command("help")

    async def on_ready(self) -> None:
        await db.init()
        self.log("Database initialized")
        
        await self.change_presence(activity=DISCORD_PRESENCE)
        self.log(f"Logged in as {self.user}")

    async def on_application_command(self, ctx: discord.ApplicationContext) -> None:
        self.log(f"{ctx.author} used {ctx.command} in {ctx.guild} (#{ctx.channel})")


# Create the bot instance
bot = Zoldicss()

# Run the bot
bot.run(DISCORD_TOKEN)