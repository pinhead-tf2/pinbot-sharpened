import discord, datetime, asyncio
from discord.ext import commands


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if ["moyai this", "moai this", "moyai react", "moai react"] in message.content:
            replyMsg = await message.channel.fetch_message(message.reference.message_id)
            await replyMsg.add_reaction("🗿")
        return


def setup(bot):
    bot.add_cog(Memes(bot))
    print("Memes loaded")


def teardown(bot):
    print('Memes unloaded')
