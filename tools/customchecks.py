import discord
from tools.config import Config

class CustomChecks():
    def checkifowner(interaction: discord.Interaction) -> bool:
        if interaction.user.id == Config.owner_id:
            return True