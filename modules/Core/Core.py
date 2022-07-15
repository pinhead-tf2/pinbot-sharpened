import discord, datetime, time
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(help="Show's the the bot's response time.")
    async def ping(self, ctx):
        await ctx.respond("**Delay:** {}ms".format(str(round(self.bot.latency*1000))), ephemeral=True)
        
    @commands.command(help="Shows how long the bot has been online for, and exactly when it started at.")
    async def uptime(self, ctx):
        await ctx.respond("**Current Uptime:** {}\n**Startup Timestamp:** <t:{}:F>".format(
            datetime.timedelta(seconds=int(time.time() - self.bot.startTime)),
            int(self.bot.startTime)
        ), ephemeral = True)
        
    # @commands.command(help="Tells you a lot of info about the bot.")
    # async def info(self, ctx):
        
        
def setup(bot):
    bot.add_cog(Core(bot))