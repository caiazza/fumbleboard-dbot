import discord
from discord.ext import commands
import logging
from datetime import datetime

__all__ = ("Bot", "bot")

class Bot(commands.Bot):
    """
    The fumble board bot basic definition
    """

    async def on_ready(self):
        logging.info(f'We have logged in as {bot.user} at {datetime.now()}')
        logging.debug(bot)


bot = Bot(command_prefix=commands.when_mentioned)
