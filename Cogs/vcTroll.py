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
                try:
                    await channel.connect(timeout=30,reconnect=False)
                    await member.guild.change_voice_state(channel=channel, self_mute=True)
                except discord.errors.ClientException:
                    pass

        elif state:
            if state.is_connected():
                await state.disconnect()

def setup(bot:commands.Bot):
    bot.add_cog(VcTroll(bot))