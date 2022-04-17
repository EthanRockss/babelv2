import discord
import json
import os
from discord.ext import commands
from configCreation import ConfigCreation

DEFAULT_CONFIG = {}

class cogManager(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    async def getEnabledCogs():
        pass

try:
    with open("Cogs/Configs/cogManager.json", "r") as config: 
        data = json.load(config)
        enabledCogs = data[]
    config.close()
except OSError as e:
    ConfigCreation.createConfig("cogManager", DEFAULT_CONFIG, True)

def getAllCogs():
    cogs = []
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            cogs.append(filename)
    return cogs

def setup(bot:commands.Bot):
    bot.add_cog(cogManager(bot))