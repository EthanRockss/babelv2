import discord
import markovify
import os
from random import randint
from discord.ext import commands
from discord.ext.commands import Context

def appendmarkovfile(text:str):
    with open("cogs/data/markov.txt", "a+", encoding="utf-8") as markov:
        markov.write(text + "\n")
    markov.close()

def generatemarkovtext() -> str:
    with open("Cogs/Data/Markov.txt", "r", encoding="utf-8") as markov:
        text = markov.read()

        textmod = markovify.Text(text)
        gentext = textmod.make_short_sentence(300)

    markov.close()
    return gentext

class Personify(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def message_sent(self, message: discord.Message):
        print("message recieved")
        if message.author.bot:
            return
        print("message passed tests")
        if message.content != None and "babel" not in message.content:
            appendmarkovfile(message.clean_content)
            print("saving message")
        if "babel" in message.content.lower():
            randnum = randint(50, 100)
        else:
            randnum = randint(-20, 80)
        print("generated number: " + str(randnum))
        if 100 >= randnum >= 75:
            gentext = generatemarkovtext()
            if gentext != None:
                try:
                    await message.channel.send(gentext)
                except discord.errors.Forbidden:
                    return

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Personify(bot))