import discord
from discord import app_commands
from discord.ext import commands
from tools.config import Config
from googleapiclient import discovery
from rcon.source import Client as rcon
from pickle import dump
from tools.customchecks import CustomChecks

service = discovery.build("compute", "v1")

project, zone, server_pass, instance, rconconf = Config.loadconfig("00111101")

def updateserverip():
	return service.instances().get(project=project, zone=zone, instance=instance).execute()["networkInterfaces"][0]["accessConfigs"][0]["natIP"]

def serverstatus() -> int:
	request = service.instances().get(project=project, zone=zone, instance=instance)
	response = request.execute()
	if response["status"] == "TERMINATED":
		return 1
	elif response["status"] == "RUNNING":
		return 2
	elif response["status"] == "STOPPING":
		return 3

class GoogleInstance(commands.Cog):
	@app_commands.command(name="status", description="status")
	async def status(self, interaction: discord.Interaction):
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

	@app_commands.command(name="start", description="start")
	async def start(self, interaction: discord.Interaction):
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

	@app_commands.check(CustomChecks.checkifowner)
	@app_commands.command(name="stop", description="stop")
	async def stop(self, interaction: discord.Interaction):
		await interaction.response.defer()
		service.instances().stop(project=project, zone=zone, instance=instance).execute()
		await interaction.followup.send("Server shutting down.")

	@app_commands.command(name="players", description="players")
	async def players(self, interaction: discord.Interaction):
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

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(GoogleInstance(bot))