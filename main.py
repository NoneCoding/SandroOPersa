import nextcord
from nextcord.ext import commands
from sandrocmd import Music
import os
from dotenv import load_dotenv

load_dotenv("key.env")

# Get API token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Create intents variable
intents = nextcord.Intents().all()

# Create bot
bot = commands.Bot(command_prefix=".", intents=intents)

# Add commands cog to bot
bot.add_cog(Music(bot))


@bot.event
async def on_ready():
    """
    When bot is ready, prints message

    """
    print("Ready! Logged as {}".format(bot.user))


# Run bot
bot.run(DISCORD_TOKEN)
