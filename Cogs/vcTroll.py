import discord
from discord.ext import commands
from gtts import gTTS
from io import BytesIO
from Tools.settingManager import addSetting, updateSetting, fetchSetting

class VcTroll(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="speak", desc="makes the bot speak when it's in the vc")
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

    @commands.is_owner()
    @commands.command(name="joinnum", desc="changed the required amount of users before the bot will join")
    async def joinnum(self, ctx:commands.Context, num:int=None):
        if num == None:
            await ctx.send("you didn't give a number of users")
        updateSetting("vctroll", "numUsers", num)
        await ctx.send(f"updated the required amount of users to {num}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        numUsers = fetchSetting("vctroll", "numUsers")
        state = discord.utils.get(self.bot.voice_clients, guild=member.guild)
        if after.channel:
            channel = after.channel
        elif before.channel:
            channel = before.channel
        if len(channel.members) >= numUsers:
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
                if len(channel.members) - 1 < numUsers:
                    await state.disconnect()

addSetting("vctroll", "numUsers", 4)

def setup(bot:commands.Bot):
    bot.add_cog(VcTroll(bot))