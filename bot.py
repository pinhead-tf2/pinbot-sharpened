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
bot.advancedUsers = [246291288775852033, 748213843615809608]
bot.startTime = time.time()
bot.version = 'Indev'
bot.releaseDate = 'Undetermined'

async def initialize():
    await bot.wait_until_ready()
    db = bot.db = await aiosqlite.connect('storage.sqlite')
    await db.execute("CREATE TABLE IF NOT EXISTS statuses(type BLOB, statustext TEXT)")
    await db.commit()
    await bot.change_presence(activity=discord.Game('Awake'), status=discord.Status.online)
    print("{} ({}) is fully online\nTime to finish: {}".format(bot.user, bot.user.id, round(time.time() - bot.startTime, 3)))

@bot.event
async def on_ready():
    if (time.time() - bot.startTime) > 60.0:
        await bot.close()
    else:
        print("{} ({}) is ready\nTime to ready: {}".format(bot.user, bot.user.id, round(time.time() - bot.startTime, 3)))
 
@bot.event
async def on_command_error(ctx: commands.Context, error):
    embed = discord.Embed(title="Command Execution Error", color=0xF04747) 
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.NotOwner):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        embed.add_field(name="Cooldown Isn't Expired", value="The command `{}` is still on cooldown! You have to wait **{} more seconds** before using this command. ({} second cooldown)".format(ctx.command, round(error.retry_after, 1), ctx.command.cooldown.per))
        embed.set_footer(text='commands.CommandOnCooldown')
    elif isinstance(error, commands.MemberNotFound):
        embed.add_field(name="Member Not Found", value="The server member `({})` you supplied for the command `{}` couldn't be found. You can use any of the following to find a server member: `userid | mention | name#tag | name | nickname`".format(error.argument, ctx.command))
        embed.set_footer(text='commands.MemberNotFound')
    elif isinstance(error, commands.UserNotFound):
        embed.add_field(name="User Not Found", value="The Discord user `({})` you supplied for the command `{}` couldn't be found. You can use any of the following to find a user: `userid | mention | name#tag | name`".format(error.argument, ctx.command))
        embed.set_footer(text='commands.UserNotFound')
    elif isinstance(error, commands.BadArgument):
        embed.add_field(name="Invalid Command Input", value="The input `{}` for the command `{}` was invalid. Consider checking the help tooltip for that command to see what works.".format(error.args, ctx.command))
        embed.set_footer(text='commands.BadArgument')
    else:
        embed = discord.Embed(title="Critical Command Execution Error", color=0xff0000)
        embed.add_field(name="Unhandled Error", value="Whoops, looks like pinhead hasn't yet coded an exception for this kind of error! I've notified him, so please be patient on waiting for a bug fix!")
        embed.set_footer(text=str(error))
        await ctx.reply(embed=embed)
        embed2 = discord.Embed(title="Command Execution Error - DM Report", color=0xff0000)
        embed2.add_field(name="New Unhandled Error", value="**Command:** {}\n**Ran by:** {} ({})\n**Error Type:** `{}`\n**Link:** {}".format(
            ctx.command,
            ctx.author.mention,
            ctx.author.name + "#" + ctx.author.discriminator,
            str(error),
            ctx.message.jump_url
        ))
        pinhead = await bot.fetch_user(246291288775852033)
        await pinhead.send(embed=embed2)
        print("\nNew Error\n")
        raise error
    return await ctx.reply(embed=embed)

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
                
        embed.add_field(name="Final Notes", value="The bot won't respond to commands it doesn't have or if you don't have permissions to use the requested command. If it won't respond at all, check the ping command and contact pinhead.")
        embed.set_footer(text="Created by pinhead#4946 | {} released {}".format(bot.version, bot.releaseDate))
        channel = self.get_destination()
        return await channel.send(embed=embed)
    
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Description", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        channel = self.get_destination()
        return await channel.send(embed=embed)

@bot.command(help="Reloads a cog. Only usable by advanced users.")
async def reload(ctx, cogName):
    try:
        bot.reload_extension(f'modules.{cogName}.{cogName}')
        await ctx.reply(f"Reloaded `modules.{cogName}.{cogName}`")
    except:
        await ctx.reply(f"Failed to load `modules.{cogName}.{cogName}`")

cogs_list = [
    'Core.Core',
    'Helpful.Helpful',
    'Statuses.Statuses',
    'Memes.Memes'
]

for cog in cogs_list:
    bot.load_extension(f'modules.{cog}')

bot.help_command = helpMe()
bot.loop.create_task(initialize())
bot.run(os.getenv('TESTTOKEN'))
asyncio.run(bot.db.close())