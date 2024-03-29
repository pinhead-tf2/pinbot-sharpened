import discord, datetime, time, platform, cpuinfo, psutil
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(help="Shuts down the bot. Only usable by the owner to safely shut down the bot during debug.")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.message.add_reaction("<:pyroThumbsUp:1008410805957566514>")
        await self.bot.close()
        
    @commands.command(help="Show's the the bot's response time.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def ping(self, ctx):
        ping = round(self.bot.latency*1000)
        if (ping <= 75):
            embcol = 0x198754
            rating = 'Excellent'
        elif (ping >= 76 and ping <= 100):
            embcol = 0x43B581
            rating = 'Good'
        elif (ping >= 101 and ping <= 200):
            embcol = 0xFAA61A
            rating = 'Moderate'
        elif (ping >= 201 and ping <= 300):
            embcol = 0xF04747
            rating = 'Poor'
        elif (ping >= 301): 
            embcol = 0xAA0000
            rating = 'Extremely Poor'
        embed = discord.Embed(title="Ping", color=embcol)
        embed.add_field(name='Discord API Response Time: {}'.format(ping), value='**Rating:** {}'.format(rating), inline=False)
        return await ctx.reply(embed=embed)
        
    @commands.command(help="Shows how long the bot has been online for, and exactly when it started at.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def uptime(self, ctx):
        uptime = int(time.time() - self.bot.startTime)
        if (uptime <= 86399): # 1 Day
            embcol = 0x198754
            rating = 'Recently Started'
        elif (uptime >= 86400 and uptime <= 604799): # 1-7 days
            embcol = 0x43B581
            rating = 'Not Needed'
        elif (uptime >= 604800 and uptime <= 1209599): # 7-14 days
            embcol = 0xFAA61A
            rating = 'Could Reboot'
        elif (uptime >= 1209600 and uptime <= 2677999): # 14-21 days
            embcol = 0xF04747
            rating = 'Reboot Soon'
        elif (uptime >= 2678000): # 31+ Days
            embcol = 0xAA0000
            rating = 'Needs Reboot'
        embed = discord.Embed(title="Uptime", color=embcol)
        embed.add_field(name='Current Uptime: {}'.format(datetime.timedelta(seconds=int(uptime))), value='**Startup Time:** {}\n**Reboot Status:** {}'.format(int(self.bot.startTime), rating), inline=False)
        return await ctx.reply(embed=embed)
        
    @commands.command(help="Tells you a lot of info about the bot and it's host.")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def info(self, ctx):
        start = time.time()
        psutil.cpu_percent() # Clear the 0.0
        embed = discord.Embed(title="Current Analytics & Info", color=ctx.author.top_role.color)
        # Bot
        embed.add_field(name="Bot Data", value="**Version:** {}\n**Release Date:** {}\n**Creator:** <@246291288775852033> (pinhead#4946)".format(self.bot.version, self.bot.releaseDate), inline=False)
        # OS
        pc = platform.uname()
        osstring = "**OS:** {} {} ({})".format(pc.system, pc.release, pc.version)
        # CPU
        cpu = cpuinfo.get_cpu_info()
        cpustring = "**CPU Model:** {} ({} GHz | {}% Load)".format(cpu['brand_raw'],
                                                               round(float(cpu['hz_advertised_friendly'][0:6]), 1), # this was so messy but fuck it
                                                               psutil.cpu_percent())
        # Mem
        memory = psutil.virtual_memory()
        available = round(memory.available/1024.0/1024.0,1)
        used = round(memory.used/1024.0/1024.0,1)
        total = round(memory.total/1024.0/1024.0,1)
        memorystring = "**Memory:** {}MB/{}MB ({}% Used | {} MB Free)".format(used, total, memory.percent, available)
        # EMBED
        embed.add_field(name="Host Computer", value="{}\n{}\n{}\n".format(osstring, cpustring, memorystring), inline=False)
        msg = await ctx.reply(embed=embed)
        embed.set_footer(text='Response Time: {} seconds'.format(round(time.time()-start, 3)))
        return await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(Core(bot))
    print('Core loaded')
    
def teardown(bot):
    print('Core unloaded')