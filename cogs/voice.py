import nextcord
from nextcord import Interaction
from nextcord.ext import commands


class voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command()
    async def connect(self, interaction: Interaction, channel: nextcord.VoiceChannel):
        if (interaction.id.voice):
            channel = interaction.author.voice.channel
            await channel.connect()
        else:
            await interaction.response.send_message("Join a voice channel to use this command")


def setup(client):
    client.add_cog(voice(client))
