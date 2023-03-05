import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands

class Utils(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	@commands.is_owner()
	async def sync(self, ctx: Context):

		ret = 0
		for guild in ctx.bot.guilds:
			try:
				await ctx.bot.tree.CommandTree.sync(self.bot, guild=guild)
			except discord.HTTPException:
				pass
			else:
				ret += 1

		await ctx.send(f"Synced the tree to {ret}/{len(ctx.bot.guilds)}.")

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

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Utils(bot))