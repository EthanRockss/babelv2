import markovify
import discord
import os
from random import randint
from discord.ext import commands

if not os.path.exists("Cogs/Data"):
    os.mkdir("Cogs/Data")

class discordMarkov(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot:
            return

        if self.bot.command_prefix in message.content:
            return

        cleanText = message.clean_content.lower()
        if message.content:
            appendMarkovText(cleanText)

        if "babel" in message.content.lower():
            randNum = randint(50,100)
        else:
            randNum = randint(0,90)
            
        if 100 >= randNum >= 85:
            genText = generateMarkovText()
            if genText:
                try:
                    await message.channel.send(str(randNum) + genText)
                except discord.errors.Forbidden as e:
                    return


def appendMarkovText(text:str):
    with open("Cogs/Data/Markov.txt", "a+", encoding='utf-8') as markov:
        markov.write(text + "\n")
    markov.close()

def generateMarkovText():
    with open("Cogs/Data/Markov.txt", "r", encoding='utf-8') as markov:
        text = markov.read()
        
    text_model = markovify.Text(text)
    genText = text_model.make_short_sentence(300)

    markov.close()
    return genText

def setup(bot:commands.Bot):
    bot.add_cog(discordMarkov(bot))