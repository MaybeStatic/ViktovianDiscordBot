import nextcord
from nextcord import Interaction
from nextcord.ext import application_checks
from nextcord.ext import commands

from main import client


class developer(commands.Cog):

    def __init__(self, client):
        self.client = client

    testServerId = 996903763770085398

    @nextcord.slash_command()
    @application_checks.has_any_role(1003142166794747965)
    async def shutdown(self, interaction: Interaction):
        if interaction.user.id != 854721351050330123:
            print(interaction.id)
            await interaction.response.send_message("You cannot use this command", ephemeral=True)
            return
        else:
            await client.close()
            await interaction.response.send_message("Shutting down")
            quit()

    @nextcord.slash_command(guild_ids=[testServerId])
    async def announce(self, interaction: Interaction, channel: nextcord.VoiceChannel, message: str):
        return await interaction.response.send_message(channel.id)

    @nextcord.slash_command(guild_ids=[testServerId])
    async def logstest(self, interaction: Interaction):
        channel = nextcord.utils.get(interaction.guild.channels, name="enginseer_logs")
        await channel.send(f"{interaction.user.mention} used the test command")
        await interaction.response.send_message("worked")


def setup(client):
    client.add_cog(developer(client))
