import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix="$", debug_guilds=[991589246949404673])

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")   
    
bot.load_extension('modules.core')

bot.run(os.getenv('TESTTOKEN'))