from discord.ext import commands
import os
from googleapiclient import discovery

#Fill these out before using
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
service = discovery.build('compute', 'v1')
project = ""
zone = ""
instance = ""

class CogName(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.group(name = "instance", description="cloud instance starter", aliases = ["ins"])
    async def instance(self, ctx):
        pass

    @commands.cooldown(1, 30, commands.BucketType.member)
    @instance.command(name = "start", description = "starts the server")
    async def start(self, ctx:commands.Context):
        request = service.instances().start(project=project, zone=zone, instance=instance)
        response = request.execute()
        if response["status"] == "RUNNING":
            gameip = getgameip(response)
            await ctx.send(f"Server Starting\njoin with 'open {gameip}'\npassword: nfa123")
        else:
            await ctx.send("Something went wrong")

    @commands.cooldown(1, 30, commands.BucketType.member)
    @instance.command(name="stop", description = "stops the server")
    async def stop(self, ctx:commands.Context):
        request = service.instances().stop(project=project, zone=zone, instance=instance)
        response = request.execute()
        await ctx.send("Server Stopping")

    @instance.command(name="status", description="check the status of the instance")
    async def status(self, ctx:commands.Context):
        request = service.instances().get(project=project, zone=zone, instance=instance)
        response = request.execute()
        if response["status"] == "TERMINATED":
            await ctx.send("Server is currently offline")
        elif response["status"] == "RUNNING":
            gameip = getgameip(response)
            await ctx.send(f"Server is online\njoin with 'open {gameip}'\npassword: nfa123")

def getgameip(response):
    ip = response["networkInterfaces"][0]["accessConfigs"][0]["natIP"]
    port = "7777"
    gameip = ip + port
    return gameip


def setup(bot:commands.Bot):
    bot.add_cog(CogName(bot))