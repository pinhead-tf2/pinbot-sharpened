import discord
from discord.ext import commands

class core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send('Welcome to my server, ' + member.mention + ' !')
        
def setup(bot):
    bot.add_cog(core(bot))