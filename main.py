import discord
import json
import os
from discord.ext import commands
from configCreation import ConfigCreation

DEFAULT_CONFIG = {
    "token": "",
    "prefix": "<",
    "owner_id": 0
}

# Attempt to get configuration file if unable create one
for i in range(5):
	try:
		with open("configuration.json", "r") as config: 
			data = json.load(config)
			token = data["token"]
			prefix = data["prefix"]
			owner_id = data["owner_id"]
	except OSError as e:
		ConfigCreation.createConfig("configuration", DEFAULT_CONFIG)


class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

# Intents
intents = discord.Intents.all()
# The bot
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)

# Load cogs
if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py"):
			bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))

bot.run(token)