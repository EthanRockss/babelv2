import sqlite3
import discord
import json
import os
from discord.ext import commands

DEFAULT_CONFIG = {
    "token": "",
    "prefix": "<",
    "owner_id": 0
}

# check to see if configuration.json file exists and if it doesn't create one
if not os.path.exists("configuration.json"):
	with open("configuration.json", "w+") as config:
		data = json.load(config)
		json.dump(DEFAULT_CONFIG, data, ensure_ascii=False, indent=4)
with open("configuration.json", "r") as config: 
	data = json.load(config)
	try:
		token = data["token"]
		prefix = data["prefix"]
		owner_id = data["owner_id"]
	except:
		print("There is a problem with your configuration file\nMake sure to include a token, prefix, and your discord id.")
		exit()

class BotCore(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None
			
# Intents
intents = discord.Intents.all()
# The bot
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)

#connect to db and create cursor
con = sqlite3.connect("Cogs/Cogs.db")
cur = con.cursor()
#create list table if it doesn't exist
cur.execute('''CREATE TABLE IF NOT EXISTS list (name, status)''')
#get list of cogs already in database
cogs = []
for row in cur.execute('''SELECT * FROM list ORDER BY name'''):
	cogs.append(row[0])
#add missing cogs to database
for c in os.listdir("Cogs/"):
	if c not in cogs and c.endswith(".py"):
		print(f"adding {c} to database")
		cur.execute('''INSERT INTO list values (?, ?)''', (c, True))
con.commit()
#load enabled cogs
cur.execute('''SELECT * FROM list WHERE status = True''')
enabledCogs = cur.fetchall()
for c in enabledCogs:
	print("loading: " + c[0])
	bot.load_extension("Cogs.{}".format(c[0][:-3]))
con.close()

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))

bot.run(token)