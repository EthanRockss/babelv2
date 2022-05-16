import sqlite3
import os
from discord.ext import commands

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
            con = sqlite3.connect("Cogs/Cogs.db")
            cur = con.cursor()
            cur.execute(f'''UPDATE list SET status = 1 WHERE name = ?''', (cog,))
            con.commit()
            con.close()
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
            con = sqlite3.connect("Cogs/Cogs.db")
            cur = con.cursor()
            cur.execute(f'''UPDATE list SET status = 0 WHERE name = ?''', (cog,))
            con.commit()
            con.close()
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

def getAllCogs():
    #connect to db and creator cursor
    con = sqlite3.connect("Cogs/Cogs.db")
    cur = con.cursor()
    enabledCogs = []
    disabledCogs = []
    for row in cur.execute('''SELECT * FROM list ORDER BY name'''):
        if row[0] == script:
            pass
        elif row[1]:
            enabledCogs.append(row[0])
        elif row[1] == False:
            disabledCogs.append(row[0])
    con.close()
    return enabledCogs, disabledCogs

def setup(bot:commands.Bot):
    bot.add_cog(cogManager(bot))