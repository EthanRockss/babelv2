from venv import create
import discord
import json
from discord.ext import commands
from Cogs.antiLeague import DEFAULT_CONFIG
from configCreation import ConfigCreation

DEFAULT_CONFIG = {"Guilds": {

    }
}

class RoleMod(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.group(name="role", desc="role")
    async def role(self, ctx):
        return

    @role.command(name = "color", desc="color")
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
            roleObj = await ctx.guild.create_role(name=ctx.author.display_name, color=hexColor)
            with open("Cogs/Configs/roleMod.json", "w") as config:
                data = {"Guilds":{ctx.guild.id:{
                    str(ctx.author.id): roleObj.id
                }}}
                json.dump(data, config, ensure_ascii=False,indent=4)
            config.close()
        await ctx.author.add_roles(roleObj)
        await ctx.send("K your role color is changed.")

    @role.command(name = "name", desc="name")
    async def rolename(self, ctx:commands.Context, *, nameStr:str):
        if not nameStr:
            await ctx.send("You didn't send anything I can use for a name")
            return
        try:
            roleId = getMemberRole(ctx.author.id, ctx.guild.id)
            roleObj = ctx.guild.get_role(roleId)
            await roleObj.edit(name=nameStr)
        except KeyError:
            roleObj = await ctx.guild.create_role(name=nameStr)
            with open("Cogs/Configs/roleMod.json", "w") as config:
                data = {"Guilds":{ctx.guild.id:{
                    str(ctx.author.id): roleObj.id
                }}}
                json.dump(data, config, ensure_ascii=False,indent=4)
            config.close()
        await ctx.author.add_roles(roleObj)
        await ctx.send("K your role name is changed.")


def getMemberRole(id:int, guildId:int):
    with open("Cogs/Configs/roleMod.json", "r") as config:
        data = json.load(config)
        roleId = data["Guilds"][str(guildId)][str(id)]
    config.close()
    return roleId

try:
    with open("Cogs/Configs/roleMod.json", "r") as config:
        data = json.load(config)
    config.close()
except OSError as e:
    ConfigCreation.createConfig("roleMod", DEFAULT_CONFIG, True)

def setup(bot:commands.Bot):
    bot.add_cog(RoleMod(bot))