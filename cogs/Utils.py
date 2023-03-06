import discord
import json
import os
import sqlite3
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands

con = sqlite3.connect("cogs/cogsettings/utils.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS logchannel (guildid, channelid)''')

class Utils(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	@commands.is_owner()
	async def sync(self, ctx: Context):
		for guild in ctx.bot.guilds:
			await ctx.bot.tree.sync(guild=guild)

	@app_commands.guild_only()
	@app_commands.checks.has_permissions(manage_messages=True)
	@app_commands.checks.bot_has_permissions(manage_messages=True)
	@app_commands.command(name="cleanup", description="deletes messages in current channel with some arguments")
	async def cleanup(self, interaction: discord.Interaction, amount: int, botonly: bool = False):
		await interaction.response.defer(ephemeral=True)
		if amount == 0:
			await interaction.followup.send("How many messages do you want me to delete?")
			return
		
		def is_me(m):
			return m.author.id == self.bot.id

		if botonly:
			await interaction.channel.purge(limit= amount, check= is_me)
		elif botonly == False:
			await interaction.channel.purge(limit= amount)

		await interaction.followup.send(f"Deleted {amount} messages.", ephemeral=True)

	@app_commands.command(name="logchannel", description="set the channel to log deleted messages to")
	@app_commands.guild_only()
	@app_commands.checks.has_permissions(manage_channels=True)
	async def logchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
		await interaction.response.defer(ephemeral=True)
		guildid = interaction.guild.id
		channelid = channel.id

		cur.execute('''SELECT * FROM logchannel WHERE guildid=?''', (guildid,))
		if cur.fetchone() != None:
			cur.execute('''SELECT * FROM logchannel WHERE guildid=?''', (guildid,))
			if cur.fetchone()[1] == channelid:
				print("no need for change")
			else:
				cur.execute('''UPDATE logchannel SET channelid=? WHERE guildid=?''', (channelid, guildid))
				print("updated")
		else:
			cur.execute('''INSERT INTO logchannel (guildid, channelid) VALUES (?, ?)''', (guildid, channelid))
			print("created new")

		await interaction.followup.send(f"Set {channel} to the log channel.", ephemeral=True)
		con.commit()

	@commands.Cog.listener("on_message_delete")
	async def message_deleted(self, message: discord.Message):
		cur.execute('''SELECT * FROM logchannel WHERE guildid=?''', (message.guild.id,))
		try:
			channelid = cur.fetchone()[1]
		except TypeError:
			return
		logchannel = discord.utils.get(message.guild.text_channels, id=channelid)
		if logchannel == None:
			return
		embedvar = discord.Embed(title="Deleted Message", description=message.clean_content, color=discord.Color.red())
		embedvar.set_author(name=f"{message.author.name}{message.author.discriminator}")
		embedvar.set_thumbnail(url=message.author.display_avatar)
		await logchannel.send(embed=embedvar)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Utils(bot))