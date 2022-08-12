import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from main import client
from nextcord.ext import application_checks

class voice(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command()
    async def connect(self, interaction:Interaction, channel:nextcord.VoiceChannel):
        if (interaction.id.voice):
            channel = interaction.author.voice.channel
            await channel.connect()
        else:
            await interaction.response.send_message("Join a voice channel to use this command")

def setup(client):
    client.add_cog(voice(client))