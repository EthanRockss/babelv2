import json
import datetime
import sqlite3
import pytz
from discord.ext import commands, tasks

DEFAULT_CONFIG = {
    "time": 15,
}

class CogName(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.check_member_status.start()

    @commands.is_owner()
    @commands.group(name = "antilegset", description="Anti League Settings group.", aliases = ["als"])
    async def antilegset(self, ctx):
        pass

    @commands.is_owner()
    @antilegset.command(name = "time", description = "Change time of Anti League Settings.")
    async def time(self, ctx:commands.Context, time:float=None):
        if not time:
            await ctx.send("No time given bro. Needs to be in minutes btw.")
            return
        con = sqlite3.connect("Cogs/Cogs.db")
        cur = con.cursor()
        cur.execute(f"UPDATE antileague SET value = {time} WHERE name = timeset")
        await ctx.send(f"Alright changing the time to {time}")
            
    @tasks.loop(seconds=30)
    async def check_member_status(self): 
        for m in self.bot.get_all_members():
            try:
                endTime = m.activities[1].start + datetime.timedelta(minutes=timeSet)
                if datetime.datetime.now(pytz.UTC).time() >= endTime.time():
                    if m.activities[1].name.lower() == "league of legends":
                        await m.send("Gross.")
                        await m.ban(delete_message_days=0, reason="Plays league of legends")
            except:
                pass

    @check_member_status.before_loop
    async def before_check_member_status(self):
        await self.bot.wait_until_ready()

con = sqlite3.connect("Cogs/Cogs.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS antileague (setting, value)''')
try:
    cur.execute('''SELECT value FROM antileague WHERE setting = timeset''')
    timeSet = cur.fetchone()[1]
except:
    cur.execute('''INSERT INTO antileague VALUES (?, ?)''', ("timeset", 30))
    timeSet = 30
con.close()

def setup(bot:commands.Bot):
    bot.add_cog(CogName(bot))