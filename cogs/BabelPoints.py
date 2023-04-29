import discord
import sqlite3
from random import randint
from discord.ext import commands
from discord import app_commands

con = sqlite3.connect("cogs/cogsettings/babpoints.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS babelpoints (guildid, userid, points)''')
cur.execute('''CREATE TABLE IF NOT EXISTS babelpointsconfig (guildid, emoji)''')

class BabelPoints(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guild_only()
    @app_commands.command()
    @app_commands.checks.has_permissions(administrator=True)
    async def bpset(self, interaction: discord.Interaction, custom_emoji: discord.Emoji):
        await interaction.response.defer(ephemeral=True)
        guildid = interaction.guild.id
        cur.execute('''SELECT * FROM babelpointsconfig WHERE guildid=?''', (guildid,))
        if cur.fetchone() != None:
             cur.execute('''UPDATE babelpointsconfig SET emoji=? WHERE guildid=?''', (custom_emoji, guildid))
        else:
             cur.execute('''INSERT INTO babelpointsconfig (guildid, emoji) VALUES (?, ?)''', (guildid, custom_emoji))

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(BabelPoints(bot))