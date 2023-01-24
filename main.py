import discord
import json
import os
from discord import app_commands
from googleapiclient import discovery

PRIMARY_GUILD = discord.Object(id=952505243072094258)

DEFAULT_CONFIG = {
    "token": "",
    "owner_id": 0,
	"project_id": "",
	"zone": "",
	"instance_name": ""
}

GAME_IP = "34.106.100.58:7777"

if not os.path.exists("configuration.json"):
	with open("configuration.json", "w+") as config:
		data = json.load(config)
		json.dump(DEFAULT_CONFIG, data, ensure_ascii=False, indent=4)
with open("configuration.json", "r") as config: 
	data = json.load(config)
	try:
		token = data["token"]
		owner_id = data["owner_id"]
		project = data["project_id"]
		zone = data["zone"]
		instance = data["instance_name"]
		os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = data["GACPath"]
	except:
		print("There is a problem with your configuration file\nMake sure to include a token and your discord id.")
		exit()

service = discovery.build("compute", "v1")

def checkifbased(interaction: discord.Interaction) -> bool:
	if interaction.user.id in [216704930831007744, 874087089828937728]:
		return True

def serverstatus() -> int:
	request = service.instances().get(project=project, zone=zone, instance=instance)
	response = request.execute()
	if response["status"] == "TERMINATED":
		return 1
	elif response["status"] == "RUNNING":
		return 2
	elif response["status"] == "STOPPING":
		return 3

class BabelClient(discord.Client):
	def __init__(self, *, intents: discord.Intents):
		super().__init__(intents=intents)
		self.tree = app_commands.CommandTree(self)

	async def setup_hook(self):
		self.tree.copy_global_to(guild=PRIMARY_GUILD)
		await self.tree.sync(guild=PRIMARY_GUILD)

intents = discord.Intents.all()
client = BabelClient(intents=intents)

@client.event
async def on_ready():
	print(f"We have logged in as {client.user}")
	print(discord.__version__)

@client.tree.command(name="status", description="check the status of the game server")
async def status(interaction: discord.Interaction):
	status = serverstatus()
	if status == 1:
		await interaction.response.send_message("The instance is not currently running.")
	elif status == 2:
		await interaction.response.send_message(f"The server is running.\nConnect via the Mordhau server browser search for `flom training grounds`.\nPassword is nfa123")
	elif status == 3:
		await interaction.response.send_message("Server is currently shutting down.")

@client.tree.command(name="start", description="start the game instance")
async def start(interaction: discord.Interaction):
	request = service.instances().start(project=project, zone=zone, instance=instance)
	response = request.execute()
	if response["status"] == "RUNNING":
		await interaction.response.send_message(f"The server is booting.\nConnect in a few minutes via the Mordhau server browser search for `flom training grounds`.\nPassword is nfa123")
	elif response["status"] == "STOPPING":
		await interaction.response.send_message("Server is currently shutting down.")
	else:
		await interaction.response.send_message("something went wrong")

@app_commands.check(checkifbased)
@client.tree.command(name="stop", description="stop the game server instance")
async def stop(interaction: discord.Interaction):
	request = service.instances().stop(project=project, zone=zone, instance=instance)
	response = request.execute()
	await interaction.response.send_message("Server shutting down.")

client.run(token)