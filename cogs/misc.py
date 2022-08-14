import datetime
import time

import nextcord
from nextcord import Interaction
from nextcord.ext import application_checks
from nextcord.ext import commands

from main import start_time


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    testServerId = 996903763770085398

    # Commands
    @nextcord.slash_command()
    async def runtime(self, interaction: Interaction):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = nextcord.Embed(colour=0xc8dc6c)
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="Viktovian Enginseer")
        try:
            await interaction.response.send_message(embed=embed)
        except nextcord.HTTPException:
            await interaction.response.send_message("Current uptime: " + text, mention_author=False)

    @nextcord.slash_command(name="roleinfo", guild_ids=[testServerId])
    async def roleinfo(self, interaction: Interaction, role: nextcord.Role):
        role_embed = nextcord.Embed(title=role, description="Info about the role", color=0xa3f0f0)
        role_embed.add_field(name="ID", value=role.id, inline=True)
        role_embed.add_field(name="Name", value=role.name, inline=True)
        role_embed.add_field(name="Hoisted", value=role.hoist, inline=True)
        role_embed.add_field(name="Position", value=role.position, inline=True)
        role_embed.add_field(name="Managed", value=role.managed, inline=True)
        role_embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
        role_embed.add_field(name="Color", value=role.color, inline=True)
        await interaction.response.send_message(embed=role_embed)

    @nextcord.slash_command(name="whois", guild_ids=[testServerId])
    async def whois(self, interaction: Interaction, member: nextcord.Member):
        avatar_1 = member.avatar.url
        whois = nextcord.Embed(title=member, description="Information about the user", color=0xa3f0f0)
        whois.add_field(name="Guild", value=member.guild, inline=True)
        whois.add_field(name="Nickname", value=member.nick, inline=True)
        whois.add_field(name="Joined at", value=member.joined_at.strftime("%m/%d/%Y"), inline=True)
        try:
            whois.add_field(name="Server Booster Since", value=member.premium_since.strftime("%m/%d/%Y"), inline=True)
        except:
            whois.add_field(name="Server Booster Since", value="Not a booster", inline=True)
        whois.set_thumbnail(url=avatar_1)
        await interaction.response.send_message(embed=whois)

    @nextcord.slash_command(name="faglist_add", description="Add a member to the faglist", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def faglist_add(self, interaction: Interaction, member: nextcord.Member):
        with open('faglist.txt', 'a') as file:
            file.write(f"{str(member.id)}\n")
            await interaction.response.send_message(f"Added {str(member)} to the faglist")

    @nextcord.slash_command(name="faglist", guild_ids=[testServerId])
    async def faglist(self, ctx):
        embed = nextcord.Embed(title="Faglist", description="Fags", color=0xa3f0f0)
        counter = 1
        with open('faglist.txt', 'r') as file:
            for line in file:
                embed.add_field(name="fag", value=f"<@{line[:-1]}>", inline=True)
                counter += 1
        await ctx.response.send_message(embed=embed)

    @nextcord.slash_command(name="avatar", description="Get the avatar of a user", guild_ids=[testServerId])
    async def avatar(self, interaction: Interaction, user: nextcord.Member):
        await interaction.response.send_message(user.avatar.url)

    @nextcord.slash_command(name="credits", description="Bot's credits", guild_ids=[testServerId]) #So I can get ma credit
    async def credits(self, interaction: Interaction):
        octo = await self.client.fetch_user(854721351050330123)
        viking = await self.client.fetch_user(713229590667067413)
        rosy = await self.client.fetch_user(568859344691527710)
        embed = nextcord.Embed(title="Credits")
        embed.add_field(name="`Created by:`", value=octo.mention)
        embed.set_footer(text="Created on: 7/24/2022")
        embed.add_field(name="`Helpers:`", value=f"{viking.mention} {rosy.mention}", inline=False)
        embed.set_thumbnail(url=octo.avatar)
        await interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(Misc(client))
