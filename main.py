import os
import time

import nextcord
from nextcord import Interaction, InteractionType
from nextcord.ext import commands
from ro_py import client
import requests

from unscsecret import token

import wolframalpha

wolframclient = wolframalpha.Client('3KY8EE-Q77HU28JQV')

start_time = time.time()
intents = nextcord.Intents.all()

intents.message_content = True

client = commands.Bot(
    command_prefix="-",

    description=None,

    help_command=None,

    case_insensitive=True,

    activity=nextcord.Game(name=f"Check out the slash(/) commands!"),

    intents=intents
)

logs = 1004003980432654336
allcogs = []
testServerId = 996903763770085398

#check discord chat
@client.slash_command(guild_ids=[testServerId])
@commands.has_any_role(1003142166794747965)
async def cogs(interaction: Interaction):
    embed = nextcord.Embed(title="Cog statuses", description="Shows the statuses of all the cogs", color=0xa3f0f0)
    for cog_name in allcogs:
        try:
            client.load_extension(f"{cog_name}")
        except commands.ExtensionAlreadyLoaded:
            embed.add_field(name=f"{cog_name[5:]}", value="✅", inline=False)
        else:
            embed.add_field(name=f"{cog_name[5:]}", value="❌", inline=False)
            client.unload_extension(f"{cog_name}")

    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.slash_command(guild_ids=[testServerId], description="Enter a problem and bot will try to answer it, if nothing pops up try to rephrase the question")
async def ask(interaction: Interaction, question:str):
    query = question
    url = f"https://api.wolframalpha.com/v1/result?appid=3KY8EE-Q77HU28JQV&i=%7Bquery%7D%3F"
    response = requests.get(url)

    if response.status_code == 501:
        await interaction.response.send_message("Unable to process")
        return

    await interaction.response.send_message(response.text)


@client.event
async def on_message(msg):
    if msg.content.startswith("-"):
        ctx = await client.get_context(msg)
        await ctx.reply(f"This bot is now using '/' commands \nView them by typing '/' and clicking on the icon on the "
                        "left", mention_author=False)
    print(f"{msg.author} said: {msg.content} \nin: {msg.channel}\n")


@client.event
async def on_member_join(member):
    print("someone joined")
    guild = member.guild
    welcome = client.get_channel(1019281615916109937)
    membercountchannel = client.get_channel(1019281423640834070)
    members = str(guild.member_count)
    print("channel found")
    if members[-1] == "1":
        members = f"{members}st"
    elif members[-1] == "2":
        members = f"{members}nd"
    elif members[-1] == "3":
        members = f"{members}rd"
    else:
        members = f"{members}th"
    msg = f"Welcome to {guild.name} {member.mention}, you are the {members} member."
    await welcome.send(msg)
    await membercountchannel.edit(name='Member count: {}'.format(membercountchannel.guild.member_count))
@client.slash_command(guild_ids=[testServerId])
async def membercount(interaction: Interaction):
    membercountchannel = client.get_channel(1006998059227553923)
    await membercountchannel.edit(name='Member count: {}'.format(membercountchannel.guild.member_count))
    await interaction.response.send_message("Updated the member count", ephemeral=True)
@client.event
async def on_ready():
    membercountchannel = client.get_channel(1006998059227553923)
    print("Bot is online")
@client.event
async def on_member_remove(member):
    guild = member.guild
    print("someone left")
    welcome = client.get_channel(997228037194125322)
    membercountchannel = client.get_channel(1006998059227553923)
    await welcome.send(f"{member.name} has left the server, member count is down to {guild.member_count}")
    await membercountchannel.edit(name='Member count: {}'.format(membercountchannel.guild.member_count))


@client.slash_command(guild_ids=[testServerId])
@commands.has_any_role(1003142166794747965)
async def load(interaction: Interaction, extension):
    try:
        client.load_extension(f"cogs.{extension}")
    except commands.ExtensionAlreadyLoaded:
        await interaction.response.send_message(f"{extension} is already loaded", ephemeral=True)
        return
    await interaction.response.send_message(f"Loaded {extension}", ephemeral=True)


@client.slash_command(guild_ids=[testServerId])
@commands.has_any_role(1003142166794747965)
async def unload(interaction: Interaction, extension):
    try:
        client.unload_extension(f"cogs.{extension}")
    except commands.ExtensionNotLoaded:
        await interaction.response.send_message(f"{extension} is already unloaded", ephemeral=True)
        return
    await interaction.response.send_message(f"Unloaded {extension}", ephemeral=True)


@client.slash_command(guild_ids=[testServerId])
@commands.has_any_role(1003142166794747965)
async def reload(interaction: Interaction, extension):
    try:
        client.unload_extension(f"cogs.{extension}")
    except commands.ExtensionNotLoaded:
        await interaction.response.send_message(f"{extension} is already unloaded", ephemeral=True)
    try:
        client.load_extension(f"cogs.{extension}")
    except commands.ExtensionAlreadyLoaded:
        await interaction.response.send_message(f"{extension} is already loaded", ephemeral=True)
    await interaction.response.send_message(f"Reloaded {extension}", ephemeral=True)

@client.slash_command(guild_ids=[testServerId])
@commands.has_any_role(1003142166794747965)
async def reload_all(interaction: Interaction):
    for acog in allcogs:
        try:
            client.unload_extension(f"{acog}")
        except commands.ExtensionNotLoaded:
            pass
        try:
            client.load_extension(f"{acog}")
        except commands.ExtensionAlreadyLoaded:
            await interaction.response.send_message(f"{acog} is already loaded", ephemeral=True)
        print(f"Reloaded {acog}")
    await interaction.response.send_message("Reloaded all extensions", ephemeral=True)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")
        allcogs.append(f"cogs.{filename[:-3]}")
@client.slash_command()
async def getchannels(interaction: Interaction):
    channels = {}
    for guild in client.guilds:
        for channel in guild.channels:
            channels.update({f"{channel.name}":channel.id})
    await interaction.response.send_message(channels, ephemeral=True)

@client.event
async def on_interaction(interaction: Interaction):
    if interaction.type == InteractionType.application_command:
        await client.process_application_commands(interaction)
        print(interaction.user)
        print(await interaction.original_message())

@client.slash_command()
async def echo(interaction:Interaction, message:str): #async def command name(interaction:Interaction) <- makes command work
    await interaction.response.send_message(message)

@client.slash_command(guild_ids=[testServerId])
async def addition(interaction : nextcord.Interaction, first:int, second:int):
    await interaction.response.send_message(f"{first + second}")


# @client.event
# async def on_message(msg):
#     user = msg.author.id
#     if user == 713229590667067413:
#         await msg.delete()





if __name__ == '__main__':
    client.run(token)

