import discord, datetime, time, platform, cpuinfo, psutil, asyncio
from discord.ext import commands

class Statuses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Statuses initialized")
        
    # @commands.Cog.listener()
    # async def on_ready(self):
        
    @commands.command(help="Toggles between splash or resource statuses. Defaults `false` for splashes.")
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def resourceStatus(self, ctx, newStatus):
        if newStatus.lower() == 'true':
            print('Resource')
        elif newStatus.lower() == 'false':
            print('Splash')
        else:
            print('Error')
            
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Command Execution Error", color=0xff0000)
            embed.add_field(name="Cooldown Isn't Expired", value="The command `{}` is still on cooldown! You have to wait **{} more seconds** before using this command. ({} second cooldown)".format(ctx.command, round(error.retry_after, 1), ctx.command.cooldown.per))
            embed.set_footer(text=str(error))
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
        
def setup(bot):
    bot.add_cog(Statuses(bot))