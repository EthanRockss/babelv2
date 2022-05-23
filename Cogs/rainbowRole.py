import sqlite3
import discord
from discord.ext import commands, tasks
from types import NoneType

class RainbowRole(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.change_role_color.start()

    @commands.command(name="setrainbow", desc="set a role to have a rainbow color")
    async def setrainbow(self, ctx, role:discord.Role):
        guildid = ctx.guild.id
        roleid = role.id
        con = sqlite3.connect("Cogs/Cogs.db")
        cur = con.cursor()
        cur.execute('''SELECT * FROM rainbowrole WHERE guildid = ? AND roleid = ?''', (guildid, roleid))
        if type(cur.fetchone()) != NoneType:
            cur.execute('''UPDATE rainbowrole SET roleid = ? WHERE guildid = ?''', (roleid, guildid))
            await ctx.send(f"Updated role to {role.mention}")
        else:
            cur.execute('''INSERT INTO rainbowrole VALUES (?,?)''', (guildid, roleid))
            await ctx.send(f"Set role to {role.mention}")
        
        con.commit()
        con.close()

    @commands.command(name="setrainbow", desc="set a role to have a rainbow color")
    async def setrainbowid(self, ctx, roleid:int=None):
        guildid = ctx.guild.id
        role = ctx.guild.get_role(roleid)
        con = sqlite3.connect("Cogs/Cogs.db")
        cur = con.cursor()
        cur.execute('''SELECT * FROM rainbowrole WHERE guildid = ? AND roleid = ?''', (guildid, roleid))
        if type(cur.fetchone()) != NoneType:
            cur.execute('''UPDATE rainbowrole SET roleid = ? WHERE guildid = ?''', (roleid, guildid))
            await ctx.send(f"Updated role to {role.mention}")
        else:
            cur.execute('''INSERT INTO rainbowrole VALUES (?,?)''', (guildid, roleid))
            await ctx.send(f"Set role to {role.mention}")
        
        con.commit()
        con.close()


    @tasks.loop(seconds=10)
    async def change_role_color(self):
        con = sqlite3.connect("Cogs/Cogs.db")
        cur = con.cursor()
        cur.execute('''SELECT * FROM rainbowrole''')
        for r in cur.fetchall():
            guild = self.bot.get_guild(r[0])
            role = guild.get_role(r[1])
            color = discord.Color.random()
            await role.edit(color=color)

    @change_role_color.before_loop
    async def before_change_role_color(self):
        await self.bot.wait_until_ready()

con = sqlite3.connect("Cogs/Cogs.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS rainbowrole (guildid, roleid)''')

con.commit()
con.close()

def setup(bot:commands.Bot):
    bot.add_cog(RainbowRole(bot))