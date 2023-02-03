from nextcord.ext import commands
from main import client
from nextcord.ext import commands

from main import client


class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    testServerId = 996903763770085398

    # Events

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id == 713229590667067413 or msg.author.id == 854721351050330123:
            if msg.content == "ban Fat fucking romanian fag":
                member = client.fetch_user(798241617118494770)
                await member.ban(reason=None)
                print("works")
                # Commands
    
    # @commands.Cog.listener()
    # async def on_message(self, msg):
    #     if "+" in msg.content:
    #         msglist = str(msg.content).split(" ")
    #         numbers = []
    #         for x in msglist:
    #             try:
    #                 numbers.append(int(x))
    #             except ValueError:
    #                 pass
    #         await msg.channel.send(sum(numbers))

  

def setup(client):
    client.add_cog(Example(client))
