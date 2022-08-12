import nextcord
from nextcord.ext import commands


class errors(commands.Cog):

    def __init__(self, client):
        self.client = client

    testServerId = 996903763770085398

    # Events
    @commands.Cog.listener()
    async def on_command_error(self, bot, error):
        with open("errorfile.txt", 'a') as file:
            if isinstance(error, commands.CommandNotFound):
                await bot.reply(error, mention_author=False)
                file.write(f"{str(error)}\n")
            elif isinstance(error, commands.errors.CommandInvokeError):
                await bot.reply(error, mention_author=False)
                file.write(f"{str(error)}\n")

            elif isinstance(error, commands.errors.MissingAnyRole):
                await bot.reply(error, mention_author=False)
                file.write(f"{str(error)}\n")

            elif isinstance(error, commands.errors.MissingRequiredArgument):
                await bot.reply(error, mention_author=False)
                file.write(f"{str(error)}\n")

            elif isinstance(error, commands.errors.TooManyArguments):
                await bot.reply(error, mention_author=False)
                file.write(f"{str(error)}\n")

            elif isinstance(error, commands.errors.MissingPermissions):
                await bot.reply(error, mention_author=False)
                file.write(f"{str(error)}\n")
            elif isinstance(error, commands.errors.MemberNotFound):
                await bot.reply(error, mention_author=False)
                file.write(f"{str(error)}\n")
            elif isinstance(error, nextcord.errors.HTTPException):
                await bot.send(error)
                with open('rareerrors.txt', 'a') as rare:
                    rare.write(f"{str(error)}\n")
            elif isinstance(error, nextcord.errors.ApplicationInvokeError):
                await bot.send(error)

    @commands.command()
    @commands.has_any_role(1003142166794747965)
    async def errors(self, ctx):
        with open('errorfile.txt') as file:
            for line in file:
                await ctx.reply(f"Current last error: {line}", mention_author=False)

    @commands.command()
    @commands.has_any_role(1003142166794747965)
    async def clearerrors(self, ctx):
        with open('errorfile.txt', 'r+') as file:
            file.truncate(0)
            file.close()
        await ctx.reply("Cleared errors", mention_author=False)


def setup(client):
    client.add_cog(errors(client))
