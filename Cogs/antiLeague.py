import json
import datetime
import pytz
from discord.ext import commands, tasks
from configCreation import ConfigCreation

DEFAULT_CONFIG = {
    "time": 15,
}

class CogName(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.check_member_status.start()

    @commands.is_owner
    @commands.group(name = "antilegset", description="Anti League Settings group.", aliases = ["als"])
    async def antilegset(self, ctx):
        pass

    @commands.is_owner
    @antilegset.command(name = "time", description = "Change time of Anti League Settings.")
    async def time(self, ctx:commands.Context, time:float=None):
        if time == None:
            await ctx.send("No time given bro. Needs to be in minutes btw.")
        else:
            EDIT_CONFIG = {
                "time": time,
            }
            with open("Cogs/Configs/antiLeagueConfig.json", "w") as config:
                json.dump(EDIT_CONFIG, config, ensure_ascii=False,indent=4)
            config.close()
            await ctx.send("Alright changing the time to {time}")
            
    @tasks.loop(seconds=30)
    async def check_member_status(self): 
        for m in self.bot.get_all_members():
            try:
                endTime = m.activities[1].start + datetime.timedelta(minutes=timeSet)
                if datetime.datetime.now(pytz.UTC).time() >= endTime.time():
                    if m.activities[1].name.lower() == "league of legends":
                        await m.send("Gross.")
                        await m.ban(delete_message_days=0, reason="Plays league of legends")
            except AttributeError as e:
                pass
            except IndexError as e:
                pass

    @check_member_status.before_loop
    async def before_check_member_status(self):
        await self.bot.wait_until_ready()

try:
    with open("Cogs/Configs/antiLeagueConfig.json", "r") as config: 
        data = json.load(config)
        timeSet = data["time"]
    config.close()
except OSError as e:
    ConfigCreation.createConfig("antiLeagueConfig", DEFAULT_CONFIG, True)

def setup(bot:commands.Bot):
    bot.add_cog(CogName(bot))