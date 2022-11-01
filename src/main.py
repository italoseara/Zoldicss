import os
import re
import asyncio
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv
from data.items import ITEMS
from utils.classes import Player
from utils.consts.emojis import EMOJIS


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


# Create the bot class
class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="\u2800",
            intents=discord.Intents.all(),
            application_id=790766945816543262,
        )

        self.load_extensions()

    def load_extensions(self) -> None:
        for extension_path in Path("cogs").glob("**/*.py"):
            if not extension_path.parts[-1].startswith("_"):
                extension_name = re.sub(
                    r"^(.+)\.py$", r"\1", str.join(".", list(extension_path.parts[1:]))
                )
                print(f"Loading extension: cogs.{extension_name}")
                self.load_extension(f"cogs.{extension_name}")
        self.remove_command("help")

    def load_emojis(self) -> None:
        GUILD_ID = 801808127388418070

        for emoji in self.get_guild(GUILD_ID).emojis:
            print(f"Loading Sprite: {emoji}")
            EMOJIS[emoji.name] = emoji

        for item in ITEMS.values():
            if item.emoji.startswith(":"):
                item.emoji = EMOJIS[item.emoji[1:-1]]

    def update_baltop(self) -> None:
        from utils.classes import db

        self.baltop = sorted(
            db.players.values(), key=lambda player: player.balance, reverse=True
        )[:10]

    async def update(self, minutes: int) -> None:
        # Update every 10 minutes
        while True:
            self.update_baltop()
            await asyncio.sleep(minutes * 60)

    async def on_ready(self) -> None:
        self.load_emojis()
        await self.change_presence(activity=discord.Game(name="Sexo 2"))

        print(f"Connected as: {self.user}")

        await self.update(5)


# Create the bot instance
bot = Bot()

# Run the bot
bot.run(TOKEN)
