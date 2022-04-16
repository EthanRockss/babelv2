import discord
import json
import time
import os
from discord.ext import commands

DEFAULT_CONFIG = {
    "time": 30,
}

class CogName(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.group(name="Anti League Defense System")
    async def antilegset(ctx):
        pass

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @antilegset.command()
    async def time(self, ctx:commands.Context, time:float=None):
        if time == None:
            ctx.send("No time given")
        
        pass

try:
    with open("babelv2/Cogs/Configs/antiLeagueConfig.json", "r") as config: 
        data = json.load(config)
        timeSet = data["time"]
        config.close()
except OSError as e:
    print("Config file not found...\nCreating...")
    with open("babelv2/Cogs/Configs/antiLeagueConfig.json", "w") as config:
        json.dump(DEFAULT_CONFIG, config, ensure_ascii=False,indent=4)
    config.close()

def setup(bot:commands.Bot):
    bot.add_cog(CogName(bot))