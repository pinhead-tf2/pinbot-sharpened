import discord, time, asyncio, aiosqlite
from discord.ext import commands
import os
from dotenv import load_dotenv

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

load_dotenv()
bot = commands.Bot(
    command_prefix=["pin ","Pin "], 
    debug_guilds=[991589246949404673], 
    help_command=commands.DefaultHelpCommand(), 
    intents=discord.Intents.all(), 
    status=discord.Status.dnd, 
    activity=discord.Game(name="Initializing...")
)
bot.startTime = time.time()
bot.version = 'Indev'
bot.releaseDate = 'Undetermined'

async def initialize():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect('storage.sqlite')
    await bot.change_presence(activity=discord.Game('Good morning, World!'), status=discord.Status.online)
    print("{} ({}) is fully online\nTime to finish: {}".format(bot.user, bot.user.id, round(time.time() - bot.startTime, 3)))
    # self.change_stats.start()

@bot.event
async def on_ready():
    print("{} ({}) is ready\nTime to ready: {}".format(bot.user, bot.user.id, round(time.time() - bot.startTime, 3)))
    
class helpMe(commands.HelpCommand):
    def get_command_signature(self, command):
        return '**%s%s %s** - %s' % ('pin ', command.qualified_name, command.signature, command.help)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_command_signature(c) for c in filtered]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
        embed.set_footer(text="Created by pinhead#4946 | {} released {}".format(bot.version, bot.releaseDate))
        channel = self.get_destination()
        return await channel.send(embed=embed)
    
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        channel = self.get_destination()
        return await channel.send(embed=embed)

cogs_list = [
    'Core.Core',
    'Helpful.Helpful',
    'Statuses.Statuses'
]

for cog in cogs_list:
    bot.load_extension(f'modules.{cog}')

bot.help_command = helpMe()
bot.loop.create_task(initialize())
bot.run(os.getenv('TESTTOKEN'))
asyncio.run(bot.db.close())