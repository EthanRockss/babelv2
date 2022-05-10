import discord
from discord.ext import commands


class VcTroll(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        state = discord.utils.get(self.bot.voice_clients, guild=member.guild)
        if after.channel:
            channel = member.voice.channel
            if len(channel.members) >= 4:
                await channel.connect(timeout=30,reconnect=False) 
        elif state.is_connected():
            await state.disconnect()

def setup(bot:commands.Bot):
    bot.add_cog(VcTroll(bot))