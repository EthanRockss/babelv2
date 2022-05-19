import discord
from discord.ext import commands
from gtts import gTTS
from io import BytesIO

class VcTroll(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="speak", desc="makes babel speak when he's in the vc")
    async def speak(self, ctx:commands.Context, *, message:str=None):
        await ctx.message.delete()
        state = discord.utils.get(self.bot.voice_clients, guild=ctx.author.guild)
        me = ctx.guild.get_member(state.user.id)

        if not message or not state:
            return

        tts = gTTS(text=message, lang="en", slow=False)
        sound_fp = BytesIO()
        tts.write_to_fp(sound_fp)

        if state.is_playing():
            return
        if me.voice.mute:
            await ctx.send(f"I WILL FUCKING MURDER YOU UNMUTE ME YOU USELESS PIECE OF FILTH {ctx.guild.owner.mention}")
            return
        if me.voice.self_mute:
            await ctx.guild.change_voice_state(channel=state.channel, self_mute=False)

        state.play(discord.FFmpegPCMAudio(sound_fp.read()), after= await ctx.guild.change_voice_state(channel=state.channel, self_mute=True))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        state = discord.utils.get(self.bot.voice_clients, guild=member.guild)
        if after.channel:
            channel = after.channel
        elif before.channel:
            channel = before.channel
        if len(channel.members) >= 4:
            try:
                await channel.connect(timeout=30,reconnect=False)
                state = discord.utils.get(self.bot.voice_clients, guild=member.guild)
                me = member.guild.get_member(state.user.id)
                if me.voice.channel:
                    await member.guild.change_voice_state(channel=channel, self_mute=True)
            except discord.errors.ClientException:
                pass
        if state:
            if state.is_connected():
                if len(channel.members) - 1 < 4:
                    await state.disconnect()

def setup(bot:commands.Bot):
    bot.add_cog(VcTroll(bot))