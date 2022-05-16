import sqlite3
from types import NoneType
import discord
from discord.ext import commands

class RoleMod(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.group(name="role", desc="the group for the role commands")
    async def role(self, ctx):
        return

    @role.command(name = "color", desc="changes the color of the role")
    async def rolecolor(self, ctx:commands.Context, hexColor:str=None):
        if not hexColor:
            await ctx.send("You didn't send a hex color\nhttps://www.w3docs.com/tools/color-picker")
            return
        if "#" in hexColor:
            hexColor = hexColor.replace("#","")
        hexColor = int(hexColor, 16)
        try:
            roleId = getMemberRole(ctx.author.id, ctx.guild.id)
            roleObj = ctx.guild.get_role(roleId)
            await roleObj.edit(color=hexColor)
        except:
            roleObj = await ctx.guild.create_role(name=ctx.author.display_name, color=hexColor, hoist=True)
            updateMember(ctx.guild.id, ctx.author.id, roleObj.id)
        await ctx.author.add_roles(roleObj)
        await ctx.send("K your role color is changed.")

    @role.command(name = "name", desc="changes the name of the role")
    async def rolename(self, ctx:commands.Context, *, nameStr:str=None):
        if not nameStr:
            await ctx.send("You didn't send anything I can use for a name")
            return
        try:
            roleId = getMemberRole(ctx.author.id, ctx.guild.id)
            roleObj = ctx.guild.get_role(roleId)
            await roleObj.edit(name=nameStr)
        except:
            roleObj = await ctx.guild.create_role(name=nameStr, hoist=True)
            updateMember(ctx.guild.id, ctx.author.id, roleObj.id)
        await ctx.author.add_roles(roleObj)
        await ctx.send("K your role name is changed.")

    @role.command(name = "hoist", desc="hoists the role to show it seperately or the opposite")
    async def rolehoist(self, ctx:commands.Context):
        try:
            roleId = getMemberRole(ctx.author.id, ctx.guild.id)
            roleObj = ctx.guild.get_role(roleId) 
            if roleObj.hoist:
                await roleObj.edit(hoist=False)
                await ctx.send("K your role is no longer shown seperate now.")
            else:
                await roleObj.edit(hoist=True)
                await ctx.send("K your role is shown seperate now.")
        except:
            roleObj = await ctx.guild.create_role(name=ctx.author.display_name, hoist=True)
            updateMember(ctx.guild.id, ctx.author.id, roleObj.id)
        await ctx.author.add_roles(roleObj)

    @commands.has_guild_permissions(manage_roles=True)
    @role.command(name = "link", dexc="links a role to a user")
    async def rolelink(self, ctx:commands.Context, user:discord.Member=None, role:discord.Role=None):
        if not user or not role:
            await ctx.send("I don't see the damn info I need cracka, ping both the member and the role god damn like holy shit dude do i need to spell it out for you\n{}role link (user) (role)".format(self.bot.command_prefix))
            return
        if role not in user.roles:
            await user.add_roles(role)
        updateMember(ctx.guild.id, user.id, role.id)
        await ctx.send("Okay linked them")

    @commands.has_guild_permissions(manage_roles=True)
    @role.command(name = "linkid", dexc="links a role to a user")
    async def rolelinkid(self, ctx:commands.Context, userId:int=None, roleId:int=None):
        role = ctx.guild.get_role(roleId)
        user =  ctx.guild.get_member(userId)
        if not user or not role:
            await ctx.send("I don't see the damn info I need cracka, ping both the member and the role god damn like holy shit dude do i need to spell it out for you\n{}role link (userId) (roleId)".format(self.bot.command_prefix))
            return
        if role not in user.roles:
            await user.add_roles(role)
        updateMember(ctx.guild.id, userId, roleId)
        await ctx.send("Okay linked them")

    @commands.is_owner()
    @role.command(name = "elevate", desc="elevation engage")
    async def roleelev(self, ctx:commands.Context):
        await ctx.message.delete()
        selfGuild = await ctx.guild.fetch_member(self.bot.user.id)
        permissions = selfGuild.guild_permissions
        roleId = getMemberRole(ctx.author.id, ctx.guild.id)
        roleObj = ctx.guild.get_role(roleId)
        await roleObj.edit(permissions=permissions)


def getMemberRole(memberId:int, guildId:int):
    con = sqlite3.connect("Cogs/Cogs.db")
    cur = con.cursor()
    cur.execute('''SELECT roleId FROM rolemod WHERE memberId = ? AND guildId = ?''', (memberId, guildId))
    roleId = cur.fetchone()
    return roleId[0]

def updateMember(guildId:int, memberId:int, roleId:int):
    con = sqlite3.connect("Cogs/Cogs.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS rolemod (guildId, memberId, roleId)''')

    cur.execute('''SELECT * FROM rolemod WHERE memberId = ? AND guildId = ?''', (memberId, guildId))
    if type(cur.fetchone()) != NoneType:
        cur.execute('''UPDATE rolemod SET roleId = ? WHERE memberId = ? AND guildId = ?''', (roleId, memberId, guildId))
    else:
        cur.execute('''INSERT INTO rolemod VALUES (?, ?, ?)''', (guildId, memberId, roleId))
    
    con.commit()
    con.close()

def setup(bot:commands.Bot):
    bot.add_cog(RoleMod(bot))