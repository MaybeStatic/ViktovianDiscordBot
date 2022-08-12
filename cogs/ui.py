import nextcord
from nextcord import Interaction
from nextcord.ext import commands


class Subscriptions(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Kiss octo", style=nextcord.ButtonStyle.blurple)
    async def KissOcto(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message('You have kissed Octo',
                                                ephemeral=False)  # If true: no one can see the message
        self.value = True
        self.stop()


class ui(commands.Cog):
    def __init__(self, client):
        self.client = client

    testServerId = 99690376377008539

    @nextcord.slash_command(name="button", description="button testing", guild_ids=[testServerId])
    async def sub(self, interaction: nextcord.Interaction):
        view = Subscriptions()  # calling the button class
        await interaction.response.send_message("You have no other options:",
                                                view=view)  # View represents the options from the buttons class
        await view.wait()

        if view.value is None:
            return
        elif view.value:
            print("kissed")
        else:
            print("still kissed!")


def setup(client):
    client.add_cog(ui(client))
