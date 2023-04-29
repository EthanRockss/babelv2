import discord
import os
import sqlite3
from random import randint
from discord.ext import commands
from discord.ext.commands import Context

con = sqlite3.connect("cogs/cogsettings/babpoints.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS babelpoints (guildid, userid, points)''')

class BabelPoints(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_guild_channel_pins_update")
    async def channel_pins_update(self, channel: discord.TextChannel, last_pin):
        print(channel.id)
        for i in await channel.pins():
            print(i.id)
        #  cur.execute('''SELECT * FROM babelpoints WHERE guildid=?''', (guildid))
        #  if cur.fetchone() != None:
        #       pass
        #  else:
        #       cur.execute('''INSERT INTO babelpoints (guildid, userid, points) VALUES (?, ?, ?)''', (guildid, userid, 1))
    

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(BabelPoints(bot))