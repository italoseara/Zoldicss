import os
import discord
from dotenv import load_dotenv

load_dotenv()

# Bot related
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_COMMAND_PREFIX = "z!"
DISCORD_APPLICATION_ID = 790766945816543262
DISCORD_INTENTS = discord.Intents(messages=True, guilds=True, members=True)
DISCORD_PRESENCE = discord.Activity(
    type=discord.ActivityType.custom,
    name="https://github.com/italoseara",
)

# Database related
DATABASE_PATH = "data/database.db"