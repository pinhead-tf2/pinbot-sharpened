import discord, datetime, time, platform, cpuinfo, psutil, asyncio, aiosqlite
from discord.ext import commands, tasks

type_cache = []
statustext_cache = []

class Statuses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statusLoop.start()
        
    def cog_unload(self):
        self.statuses.cancel()
        
    @tasks.loop(minutes=1.0)
    async def statusLoop(self):
        print("Status")

    @statusLoop.before_loop
    async def beforeReady(self):
        await self.bot.wait_until_ready()
        db = self.bot.db
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM statuses") as cursor:
            print(await cursor.fetchone())
            
    @commands.command(help="Adds a status to the bot's status database. Only usable by the owner.")
    # @commands.is_owner()
    async def addstatus(self, ctx, type, *statustext):
        type = type.lower()
        if type == "playing":
            type = discord.ActivityType.playing
        elif type == "listening":
            type = discord.ActivityType.listening
        elif type == "watching":
            type = discord.ActivityType.watching
        else:
            print("idk yet")
        
        db = self.bot.db
        cursor = await db.cursor()
        await cursor.execute(f"INSERT INTO statuses(type, statustext) VALUES(?, ?)", (type, statustext))
        type_cache.append(type)
        statustext_cache.append(statustext)
        embed = discord.Embed(title="New Status Added", color=0x43B581)
        embed.add_field(name="Activity Type", value="{}".format(type), inline=False)
        embed.add_field(name="Activity Text", value="{}".format(statustext), inline=False)
        embed.set_footer(text="Status ID: {}".format(cursor.lastrowid()))
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Statuses(bot))
    print("Statuses loaded")
    
def teardown(bot):
    print('Statuses unloaded')