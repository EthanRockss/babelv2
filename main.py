import discord
import json
import os
from discord import app_commands
from Tools.settingManager import createSetTable
from googleapiclient import discovery

#Fill these out before using
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
service = discovery.build('compute', 'v1')
project = ""
zone = ""
instance = ""

createSetTable()

TESTING_GUILD = discord.Object(id=596781722448822282)

DEFAULT_CONFIG = {
    "token": "",
    "owner_id": 0
}

# check to see if configuration.json file exists and if it doesn't create one
if not os.path.exists("configuration.json"):
	with open("configuration.json", "w+") as config:
		data = json.load(config)
		json.dump(DEFAULT_CONFIG, data, ensure_ascii=False, indent=4)
with open("configuration.json", "r") as config: 
	data = json.load(config)
	try:
		token = data["token"]
		owner_id = data["owner_id"]
	except:
		print("There is a problem with your configuration file\nMake sure to include a token and your discord id.")
		exit()

class BabelClient(discord.Client):
	def __init__(self, *, intents: discord.Intents):
		super().__init__(intents=intents)
		self.tree = app_commands.CommandTree(self)

	async def setup_hook(self):
		self.tree.copy_global_to(guild=TESTING_GUILD)
		await self.tree.sync(guild=TESTING_GUILD)

@app_commands.guild_only()
class instance(app_commands.Group(name="instance", description="commands to control the game server instance")):
	pass

@instance.command(name="status", description="a command to check the current status of the game server instance")
async def status(interaction: discord.Interaction):
	interaction.response.send_message("")

intents = discord.Intents.all()
client = BabelClient(intents=intents)

@client.event
async def on_ready():
	print(f"We have logged in as {client.user}")
	print(discord.__version__)

client.run(token)