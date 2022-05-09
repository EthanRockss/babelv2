import discord
import json
import os
from discord.ext import commands
from configCreation import ConfigCreation

DEFAULT_CONFIG = {}

script = os.path.basename(__file__)

class cogManager(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name = "load", description="load cog")
    async def load(self, ctx:commands.Context, cog:str=None):
        if cog == None:
            await ctx.send("Dude what cog do you want me to load.")
            return
        if not cog.endswith(".py"):
            cog = cog + ".py"
        if cog not in os.listdir("Cogs") or cog == script:
            await ctx.send("Dude what cog do you want me to load.")
            return
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
        if cog == None:
            await ctx.send("Dude what cog do you want me to unload.")
            return
        if not cog.endswith(".py"):
            cog = cog + ".py"
        if cog not in os.listdir("Cogs") or cog == script:
            await ctx.send("Dude what cog do you want me to unload.")
            return
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
        enabledCogs, disabledCogs = getAllCogs()
        if not enabledCogs and not disabledCogs:
            await ctx.send("there is no available cogs")
            return
        if enabledCogs:
            messageOne = ", ".join(enabledCogs)
        else:
            messageOne = "No enabled cogs."
        if disabledCogs:
            messageTwo = ", ".join(disabledCogs)
        else:
            messageTwo = "No disabled cogs."
        await ctx.send("```Enabled:\n{}```\n```Disabled:\n{}```".format(messageOne, messageTwo).replace(".py",""))

for i in range(5):
    try:
        with open("cogConfig.json", "r") as config: 
            data = json.load(config)
        config.close()
    except OSError as e:
        ConfigCreation.createConfig("cogConfig", DEFAULT_CONFIG, False)

def getAllCogs():
    enabledCogs = []
    disabledCogs = []
    with open("cogConfig.json", "r") as config:
        data = json.load(config)
        for i in data["Cogs"]:
            if i == script:
                pass
            elif data["Cogs"][i]:
                enabledCogs.append(i)
            elif not data["Cogs"][i]:
                disabledCogs.append(i)
    return enabledCogs, disabledCogs

def setup(bot:commands.Bot):
    bot.add_cog(cogManager(bot))