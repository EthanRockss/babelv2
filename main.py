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

COG_CONFIG = {
	"Cogs": {

	}
}

for filename in os.listdir("Cogs"):
	if filename.endswith(".py"):
		COG_CONFIG["Cogs"][filename] = True

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


class BotCore(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

	@commands.is_owner()
	@commands.command(name = "load", description="load cog")
	async def load(self, ctx:commands.Context, cog:str=None):
		if not cog.endswith(".py"):
			cog.append(".py")
		if cog == None or cog not in os.listdir("Cogs"):
			await ctx.send("Dude what cog do you want me to load.")
		else:
			try:
				bot.load_extension(f"Cogs.{cog}")
				with open("cogConfig.json", "r") as config:
					data = json.load(config)
					data["Cogs"][cog] = True
					json.dump(data, config, ensure_ascii=False, indent=4)
			except commands.errors.ExtensionNotFound:
				await ctx.send("that cog is already loaded bro.")
			
				
		

# Intents
intents = discord.Intents.all()
# The bot
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)

# Load cogs
try:
	with open("cogConfig.json", "r") as config: 
		data = json.load(config)
		cogs = data["Cogs"]
		config.close()
	failedCogs = []
	for i in cogs:
		try:
			bot.load_extension(f"Cogs.{i[:-3]}")
		except commands.errors.ExtensionNotFound:
			if i not in os.listdir("Cogs"):
				failedCogs.append(i)
	for i in failedCogs:
		cogs.pop(i, None)
		with open("cogConfig.json", "r") as config:
			json.dump(cogs, config, ensure_ascii=False, indent=4)
except OSError as e:
	ConfigCreation.createConfig("cogConfig", COG_CONFIG)

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))

bot.run(token)