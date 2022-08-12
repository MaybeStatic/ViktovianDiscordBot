from code import interact
from ro_py import Client
import nextcord
from nextcord.ext import commands
from ro_py.thumbnails import ThumbnailSize, ThumbnailType
from main import secret, client
from nextcord import Interaction, SlashOption
from nextcord.ext import application_checks
import time,datetime
import ro_py
from ro_py import utilities

roblox = Client(secret)

class RobloxCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    testServerId = 996903763770085398

    @nextcord.slash_command(name="finduser", description="Look up a user from roblox with their username", guild_ids=[testServerId]) #Rememberrr
    async def finduser(self, interaction:Interaction, *, username):
        # if type(username) == discord.member.Member:
        #     username = username.nick.split(" ",1) [0]
        user = await roblox.get_user_by_username(username)
        embed = nextcord.Embed(title=f"Info for {user.name}")
        status = await user.get_status()
        embed.add_field(
            name="Username",
            value="`" + user.name + "`",
            inline=False
        )
        embed.add_field(
            name="Display Name",
            value="`" + user.display_name + "`",
            inline = False
        )
        embed.add_field(
            name="User ID",
            value="`" + str(user.id) + "`",
            inline = False
        )
        embed.add_field(
            name="Joined on",
            value="`" + user.created.strftime("%m/%d/%Y") + "`",
            inline = False
        )
        embed.add_field(
            name="Description",
            value="```" + ((user.description or "No description")) + "```",
            inline = True
        )
        avatar_image = await user.thumbnails.get_avatar_image(
        shot_type=ThumbnailType.avatar_headshot,  # headshot
        size=ThumbnailSize.size_420x420,  # high resolution thumbnail
        is_circular=False  # square thumbnail
        )
        embed.set_thumbnail(
            url=avatar_image
        )
        await interaction.response.send_message(embed=embed)
    
    @nextcord.slash_command(name="shout", description="Send a shout to the group via the bot", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def shout(self, interaction:Interaction, *, shout_text):
        group = await roblox.get_group(15614750)  # Group ID here
        await group.shout(shout_text)
        await interaction.response.send_message("Sent shout.")
    
    @nextcord.slash_command(name="exile", description="Exiles a user", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def exile(self, interaction:Interaction, member:nextcord.Member):
        try: 
            realuser = member.nick.split(" ", 1)[0]
        except:
            realuser = member.nick
        group = await roblox.get_group(15614750)  # Group ID here
        member = await group.get_member_by_username(realuser)
        await member.exile()
        embed = nextcord.Embed(title=f"Rank update:", description=f"{realuser} has been demoted", color=0xa3f0f0)
        await interaction.response.send_message(embed=embed)
    
    @nextcord.slash_command(name="promote", description="Promotes a user", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def promote(self, interaction:Interaction, member:nextcord.Member):
        try: 
            realuser = member.nick.split(" ", 1)[0]
        except:
            realuser = member.nick
        group = await roblox.get_group(15614750)  # Group ID here
        member = await group.get_member_by_username(realuser)
        try: 
            await member.promote()
        except utilities.errors.NotFound:
            interaction.response.send_message(f"{member.name} not in the group")
        embed = nextcord.Embed(title=f"Rank update:", description=f"{realuser} has been promoted", color=0xa3f0f0)
        await interaction.response.send_message(embed=embed)
    
    @nextcord.slash_command(name="demote", description="Demotes a user", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def demote(self, interaction:Interaction, member:nextcord.Member):
        try: 
            realuser = member.nick.split(" ", 1)[0]
        except:
            realuser = member.nick
        group = await roblox.get_group(15614750)  # Group ID here
        member = await group.get_member_by_username(member.nick.split(" ", 1)[0])
        await member.demote()
        embed = nextcord.Embed(title=f"Rank update:", description=f"{realuser} has been demoted", color=0xa3f0f0)
        await interaction.response.send_message(embed=embed)
    @nextcord.slash_command(name="setrank", description="Set the rank of a user", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def setrank(self, interaction:Interaction, username:nextcord.Member, rank: int=SlashOption(
        name="rank",
        choices={"Legatus":16,"Laticlavius":15,"Praefectus":14,"Tribunus":13,"Centurio":12,"Optio":10,"Salarius":9,"Triplicarius":8,"Duplicarius":7,"Sesquiplicarius":6,"Immunis":4,"Discens":3, "Miles":2,"Tiro":1}
    )):
        try: 
            realuser = username.nick.split(" ", 1)[0]
        except:
            realuser = username.nick
        print(realuser)
        print(rank)
        if 255 >= rank >= 1:  # Make sure rank is in allowed range
            group = await roblox.get_group(15614750)  # Group ID here
            member = await group.get_member_by_username(realuser)
            await member.setrole(rank)  # Sets the rank
            await interaction.response.send_message("Promoted user.")
        else:
            await interact("Rank must be at least 1 and at most 255.")
    @nextcord.slash_command(name="groupinfo", description="Get information about a group with the ID")
    async def groupinfo(self, interaction:Interaction, groupid:int):
        group = await roblox.get_group(groupid)
        embed = nextcord.Embed(title=f"{group.name}", color=0xa3f0f0)

        embed.add_field(
            name="Group ID",
            value=(group.id),
            inline=True
        )

        embed.add_field(
            name="Description",
            value=(group.description or "n/a"),
            inline=False
        )

        embed.add_field(
            name="Member Count",
            value=(group.member_count),
            inline=True
        )

        embed.add_field(
            name="Owner",
            value=(group.owner.name),
            inline=True
        )

        embed.add_field(
            name="Group Shout",
            value=(group.shout or "N/A"),
            inline=True
        )

        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command()
    @application_checks.has_any_role(1003142166794747965)
    async def victory(self, interaction:Interaction, group:int, group_icon:str, score:str, image_link:str):
        group = await roblox.get_group(group)
        victorychannel = self.client.get_channel(1001599817220358234)
        embed = nextcord.Embed(
            title=f"Viktovia vs {group.name}", 
            description="Result: **Victory**",
            type="image"
        )

        embed.set_image(url=image_link)
        embed.set_thumbnail(url=group_icon)
        embed.add_field(
            name="Score",
            value="`"+score+"`",
            inline=True
        )
        await victorychannel.send(embed=embed)
        await interaction.response.send_message(f"{group.name} {victorychannel}")

def setup(client):
    client.add_cog(RobloxCommands(client))