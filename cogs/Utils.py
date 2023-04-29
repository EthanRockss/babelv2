import discord
import sqlite3
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands

con = sqlite3.connect("cogs/cogsettings/utils.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS logchannel (guildid, channelid)''')

def getchannelid(guild_id: int) -> int:
	cur.execute('''SELECT * FROM logchannel WHERE guildid=?''', (guild_id,))
	try:
		channelid = cur.fetchone()[1]
	except TypeError:
		return
	return channelid

class Utils(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	@commands.is_owner()
	async def sync(self, ctx: Context):
		for guild in ctx.bot.guilds:
			coms = await ctx.bot.tree.sync(guild=guild)
			await ctx.send(f"Synced {len(coms)} to {guild.name}")

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
			if cur.fetchone()[1] != channelid:
				cur.execute('''UPDATE logchannel SET channelid=? WHERE guildid=?''', (channelid, guildid))
		else:
			cur.execute('''INSERT INTO logchannel (guildid, channelid) VALUES (?, ?)''', (guildid, channelid))

		await interaction.followup.send(f"Set {channel} to the log channel.", ephemeral=True)
		con.commit()

	@commands.Cog.listener("on_message_delete")
	async def message_deleted(self, message: discord.Message):
		if message.author.bot == True:
			return
		logchannel = discord.utils.get(message.guild.text_channels, id=getchannelid(message.guild.id))
		embedvar = discord.Embed(title="Deleted Message", color=discord.Color.red())
		embedvar.set_author(name = message.author.name + message.author.discriminator)
		embedvar.set_thumbnail(url=message.author.display_avatar)
		embedvar.add_field(name="Message Contents", value=message.clean_content)
		if len(message.attachments) > 0:
			oldfiles = []
			for i in message.attachments:
				oldfiles.append(await i.to_file(spoiler=i.is_spoiler()))
			await logchannel.send(embed=embedvar, files=oldfiles)
		else:
			await logchannel.send(embed=embedvar)

	@commands.Cog.listener("on_message_edit")
	async def message_edited(self, before: discord.Message, after: discord.Message):
		if before.author.bot == True:
			return
		if before.clean_content == after.clean_content:
			return
		logchannel = discord.utils.get(before.guild.text_channels, id=getchannelid(before.guild.id))
		embedvar = discord.Embed(title="Edited Message", color=discord.Color.orange())
		embedvar.set_author(name = before.author.name + before.author.discriminator)
		embedvar.set_thumbnail(url=before.author.display_avatar)
		embedvar.add_field(name="Before", value=before.clean_content)
		embedvar.add_field(name="After", value=after.clean_content)
		await logchannel.send(embed=embedvar)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Utils(bot))