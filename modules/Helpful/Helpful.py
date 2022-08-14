from socket import timeout
import discord, datetime, asyncio
from discord.ext import commands

class Helpful(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Helpful initialized")
        
    @commands.command(help="Gives you the profile picture of a user. Returns yours if left blank.", aliases=['pfp'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def avatar(self, ctx, *, user = None):
        if user is None:
            member = ctx.author
        else:
            try:
                member = await commands.MemberConverter().convert(ctx, user)
            except:
                reactMsg = await ctx.send("The user you requested couldn't be found in this server. Spread search to any matching Discord member?\n*15 seconds to answer.*")
                await reactMsg.add_reaction('✅')
                await reactMsg.add_reaction('❌')
                
                def check(reaction, usr):
                    return usr == ctx.author and str(reaction.emoji) in ['✅', '❌']

                try:
                    reaction = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    await reactMsg.delete()
                    return await ctx.reply("No reaction.")
                else:
                    if str(reaction[0].emoji) == '✅':
                        member = await commands.UserConverter().convert(ctx, user)
                    else:
                        await reactMsg.delete()
                        return await ctx.reply("Command cancelled.")
        embed = discord.Embed(title="Avatar", description="Here's {}'s avatar!".format(member.name), color=member.top_role.color)
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text='As of {}'.format(datetime.datetime.now().strftime("%I:%M:%S %p %m/%d/%Y")))
        await ctx.reply(embed=embed)
        
def setup(bot):
    bot.add_cog(Helpful(bot))