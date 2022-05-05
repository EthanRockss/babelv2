import discord
import json
import os
from discord.ext import commands
from configCreation import ConfigCreation

DEFAULT_CONFIG = {}

class cogManager(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name = "load", description="load cog")
    async def load(self, ctx:commands.Context, cog:str=None):
        if cog == None or cog not in os.listdir("Cogs"):
            await ctx.send("Dude what cog do you want me to load.")
            return
        if not cog.endswith(".py"):
            cog.append(".py")
        try:
            self.bot.load_extension(f"Cogs.{cog[:-3]}")
            with open("cogConfig.json", "r") as config:
                data = json.load(config)
                data["Cogs"][cog] = True
                config.close()
            with open("cogConfig.json", "w") as config:
                json.dump(data, config, ensure_ascii=False, indent=4)
        except commands.errors.ExtensionAlreadyLoaded:
            await ctx.send("that cog is already loaded bro.")

    @commands.is_owner()
    @commands.command(name = "unload", description="unload cog")
    async def unload(self, ctx:commands.Context, cog:str=None):
        if cog == None or cog not in os.listdir("Cogs"):
            await ctx.send("Dude what cog do you want me to unload.")
            return
        if not cog.endswith(".py"):
            cog.append(".py")
        try:
            self.bot.unload_extension(f"Cogs.{cog[:-3]}")
            with open("cogConfig.json", "r") as config:
                data = json.load(config)
                data["Cogs"][cog] = False
                config.close()
            with open("cogConfig.json", "w") as config:
                json.dump(data, config, ensure_ascii=False, indent=4)
        except commands.errors.ExtensionNotLoaded:
            await ctx.send("that cog is already unloaded bro.")

    @commands.is_owner()
    @commands.command(name = "cogs", description="see list of cogs")
    async def cogs(self, ctx:commands.Context):
        cogs = getAllCogs()
        if not cogs:
            await ctx.send("there is no available cogs")
            return
        message = ", ".join(cogs)
        await ctx.send("```{}```".format(message))


for i in range(5):
    try:
        with open("cogConfig.json", "r") as config: 
            data = json.load(config)
            enabledCogs = data["Cogs"]
        config.close()
    except OSError as e:
        ConfigCreation.createConfig("cogConfig", DEFAULT_CONFIG, False)

def getAllCogs():
    cogs = []
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            cogs.append(filename)
    return cogs

def setup(bot:commands.Bot):
    bot.add_cog(cogManager(bot))