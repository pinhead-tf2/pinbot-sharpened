from types import NoneType
import discord, datetime
from discord.ext import commands

class Helpful(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Helpful initialized")
        
    @commands.command(help="Gives you the profile picture of a user, returns yours if left blank.", aliases=['pfp'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def avatar(self, ctx, target = None):
        if target is None:
            userref = ctx.author
        elif target.isdigit():
            try:
                userref = await self.bot.get_or_fetch_user(int(target))
            except:
                return await noUserFound(self, ctx, errorType, target)
        elif target is discord.Member:
            userref = target
        else: 
            return print("invalid input")
        print('Still ran')
        # embed = discord.Embed(title="Avatar", description="Here's {}'s avatar!".format(userref.name), color=userref.top_role.color)
        # embed.set_image(url=userref.display_avatar.url)
        # embed.set_footer(text='As of {}'.format(datetime.datetime.now().strftime("%H:%M:%S %m/%d/%Y")))
        # await ctx.reply(embed=embed)
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Command Execution Error", color=0xff0000)
            embed.add_field(name="Cooldown Isn't Expired", value="The command `{}` is still on cooldown! You have to wait **{} more seconds** before using this command. ({} second cooldown)".format(ctx.command, round(error.retry_after, 1), ctx.command.cooldown.per))
            embed.set_footer(text='commands.CommandOnCooldown')
            return await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="Command Execution Error", color=0xff0000)
            embed.add_field(name="Unhandled Error", value="Whoops, looks like pinhead hasn't yet coded an exception for this kind of error! I've notified him, so please be patient on waiting for a bug fix!")
            embed.set_footer(text=str(error))
            await ctx.reply(embed=embed)
            embed = discord.Embed(title="Command Execution Error - DM Report", color=0xff0000)
            embed.add_field(name="New Unhandled Error", value="**Command:** {}\n**Ran by:** {} ({})\n**Error Type:** `{}`\n**Link:** {}".format(
                ctx.command,
                ctx.author.mention,
                ctx.author.name + "#" + ctx.author.discriminator,
                str(error),
                ctx.message.jump_url
            ))
            pinhead = await self.bot.get_or_fetch_user(246291288775852033)
            await pinhead.send(embed=embed)
            raise error
        
async def noUserFound(errorType, self, ctx, input):
    print("bad")
        
def setup(bot):
    bot.add_cog(Helpful(bot))