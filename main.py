import discord
import json
import os
from discord import app_commands
from googleapiclient import discovery
from rcon.source import Client as rcon
from pickle import dump

DEFAULT_CONFIG = {
    "token": "",
    "owner_id": 0,
	"project_id": "",
	"zone": "",
	"instance_name": "",
	"server_pass": "",
	"gac_path": "",
	"primary_guild": 0,
	"rcon": {
		"password": "",
		"port": 0
	}
}

if not os.path.exists("configuration.json"):
	with open("configuration.json", "w", encoding="utf-8") as config:
		json.dump(DEFAULT_CONFIG, config, ensure_ascii=False, indent=4)
		print("please fill out the configuration file.")
		exit()
with open("configuration.json", "r") as config: 
	data = json.load(config)
	try:
		token = data["token"]
		owner_id = data["owner_id"]
		project = data["project_id"]
		zone = data["zone"]
		server_pass = data["server_pass"]
		instance = data["instance_name"]
		os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = data["gac_path"]
		PRIMARY_GUILD = discord.Object(id=data["primary_guild"])
		rconconf = data["rcon"]
	except:
		print("There is a problem with your configuration file\nMake sure to include a token and your discord id.")
		exit()

service = discovery.build("compute", "v1")

def updateserverip():
	return service.instances().get(project=project, zone=zone, instance=instance).execute()["networkInterfaces"][0]["accessConfigs"][0]["natIP"]

def checkifbased(interaction: discord.Interaction) -> bool:
	if interaction.user.id == owner_id:
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
	await interaction.response.defer()
	status = serverstatus()
	if status == 1:
		await interaction.followup.send("The instance is not currently running.")
	elif status == 2:
		await interaction.followup.send(f"The server is running.\nConnect via the Mordhau server browser search for `flom training grounds`.\nPassword is `{server_pass}`")
	elif status == 3:
		await interaction.followup.send("Server is currently shutting down.")
	else:
		await interaction.followup.send("something went wrong")

@client.tree.command(name="start", description="start the game instance")
async def start(interaction: discord.Interaction):
	await interaction.response.defer()
	request = service.instances().start(project=project, zone=zone, instance=instance)
	response = request.execute()
	with open("prev_check.pk", "w+b") as fi:
		dump(False, fi)
	fi.close()
	if response["status"] == "RUNNING":
		await interaction.followup.send(f"The server is booting.\nConnect in a few minutes via the Mordhau server browser search for `flom training grounds`.\nPassword is `{server_pass}`")
	elif response["status"] == "STOPPING":
		await interaction.followup.send("Server is currently shutting down.")
	else:
		await interaction.followup.send("something went wrong")

@app_commands.check(checkifbased)
@client.tree.command(name="stop", description="stop the game server instance")
async def stop(interaction: discord.Interaction):
	await interaction.response.defer()
	service.instances().stop(project=project, zone=zone, instance=instance).execute()
	await interaction.followup.send("Server shutting down.")

@client.tree.command(name="players", description="get list of players on the server")
async def players(interaction: discord.Interaction):
	await interaction.response.defer()
	statuscheck = serverstatus()
	if statuscheck == 1 or statuscheck == 3:
		await interaction.followup.send("The server is currently offline.")
		return
	server_ip = updateserverip()
	try:
		with rcon(server_ip, rconconf["port"], passwd=rconconf["password"]) as connection:
			response = connection.run('playerlist')
	except:
		await interaction.followup.send("something went wrong.")
		return

	players = int
	playerlist = ""

	if response.startswith("There are currently no players present"):
		players = 0
	else:
		players = response.count("\n")
		for i in response.split("\n"):
			p = i.split(", ")
			if len(p) > 1:
				playerlist = playerlist + f"{p[1]}\n"
		
	if len(playerlist) > 1:
		await interaction.followup.send(f"There are {players} players online\nCurrent players:\n```{playerlist}```")
	else:
		await interaction.followup.send(f"There are no players online.")

@app_commands.guild_only()
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.checks.bot_has_permissions(manage_messages=True)
@client.tree.command(name="cleanup", description="clean up messages")
async def cleanup(interaction: discord.Interaction, amount: int, botonly: bool = False):
	await interaction.response.defer(ephemeral=True)
	if amount == 0:
		await interaction.followup.send("How many messages do you want me to delete?")
		return
	
	def is_me(m):
		return m.author == client.user

	if botonly:
		await interaction.channel.purge(limit= amount, check= is_me)
	elif botonly == False:
		await interaction.channel.purge(limit= amount)

	await interaction.followup.send(f"Deleted {amount} messages.", ephemeral=True)

client.run(token)