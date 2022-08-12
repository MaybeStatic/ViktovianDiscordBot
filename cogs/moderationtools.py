import nextcord
from nextcord import Interaction
from nextcord.ext import application_checks
from nextcord.ext import commands

from main import client


class moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    testServerId = 996903763770085398

    # Commands
    # Rememberrr
    @nextcord.slash_command(name="ban", description="Bans a user from the server", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def ban(self, interaction: Interaction, member: nextcord.Member, *, reason=None):
        if member == None:
            await interaction.response.send_message("You cannot ban yourself")
            return
        if reason == None:
            reason = "For being a jerk!"
        await member.ban(reason=reason)
        embed = nextcord.Embed(title=f'User {member} has been banned')
        await interaction.response.send_message(embed=embed)
        print(f"banned {member}")

    @nextcord.slash_command(name="showchannel")
    @application_checks.has_any_role(1003142166794747965)
    async def checkchannel(self, interaction: Interaction):
        logs = self.client.get_channel(1004003980432654336)
        await logs.send("worked")
        await interaction.response.send_message("Worked")

    @nextcord.slash_command(name="kick", description="Kick a user from the server", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def kick(self, interaction: Interaction, member: nextcord.Member, reason=None):
        if member == None or member.id == interaction.user.id:
            await interaction.response.send_message("You cannot kick yourself", ephemeral=True)
            return
        if member.has_permissions(administrator=True):
            await interaction.response.send_message("Cannot kick an administrator")
        if reason == None:
            reason = "For being a jerk!"
        await member.kick(reason=reason)
        embed = nextcord.Embed(title=f'User {member} has been kicked')
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="unban", guild_ids=[testServerId])
    @commands.has_any_role(1003142166794747965)
    async def unban(self, interaction, member_id):
        username = client.get_user(member_id)
        await client.unban(nextcord.Object(id=member_id))
        embed = nextcord.Embed(title=f'User {username} has been unbanned')

    @nextcord.slash_command(name="purge", description="Mass deletes messgaes from the server", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def purge(self, interaction: Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Purged {amount} messgaes", ephemeral=True)

    @nextcord.slash_command(name="softban", description="Bans and unbans a user so their messages may be deleted",
                            guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def softban(self, interaction: Interaction, *, member: nextcord.Member):
        user = await client.fetch_user(interaction.id)
        await member.send(
            f"You have been softbanned in order to delete your messages, please rejoin:\nhttps://discord.gg/viktovia")
        await member.ban(reason=None)
        await user.unban()
        await interaction.response.send_message(f"{member} softbanned")

    @nextcord.slash_command(name="roleadd", description="Adds a role to the user", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def giverole(self, interaction: Interaction, member: nextcord.Member, role: nextcord.Role):
        await member.add_roles(role)
        await interaction.response.send_message(f"Gave the {role} role to {member}")

    @nextcord.slash_command(name="removerole", description="Removes a role from the user", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def removerole(self, interaction: Interaction, member: nextcord.Member, role: nextcord.Role):
        await member.remove_roles(role)
        await interaction.response.send_message(f"Removed the {role} role from {member}")

    @nextcord.slash_command(name="members", description="get all the members in the guild", guild_ids=[testServerId])
    @application_checks.has_any_role(1003142166794747965)
    async def members(self, interaction: Interaction):
        members = list(client.get_all_members())
        print(members)


def setup(client):
    client.add_cog(moderation(client))
