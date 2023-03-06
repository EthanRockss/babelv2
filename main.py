import discord
from discord import app_commands
from tools.config import Config
from discord.ext import commands
from tools.customchecks import CustomChecks

token, PRIMARY_GUILD = Config.loadconfig("10000010")

class BabelClient(commands.Bot):
	def __init__(self):
		intents = discord.Intents().all()
		super().__init__(command_prefix=commands.when_mentioned,
		   				 intents=intents)
		
		self.initial_extensions = ["cogs.GoogleInstance", "cogs.Utils"]

	async def setup_hook(self):
		for i in self.initial_extensions:
			await self.load_extension(i)

	async def on_ready(self):
		print(f"We have logged in as {self.user}")
		print(discord.__version__)

bot = BabelClient()
bot.run(token)