import markovify
import discord
from random import randint
from discord.ext import commands


class discordMarkov(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot:
            return

        cleanText = message.clean_content.lower()
        if message.content:
            appendMarkovText(cleanText)

        randNum = randint(0,100)
        if 100 <= randNum >= 90:
            genText = generateMarkovText()
            if genText:
                await message.channel.send(genText)


def appendMarkovText(text:str):
    with open("Cogs/Data/Markov.txt", "a", encoding='utf-8') as markov:
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