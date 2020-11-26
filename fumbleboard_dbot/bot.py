import discord
from discord.ext import commands
import logging
from datetime import datetime
import fumbleboard_dbot.tracklist
# from fumbleboard_dbot.tracklist import Tracklist
import json

__all__ = ("Bot", "bot")

class Bot(commands.Bot):
    """
    The fumble board bot basic definition
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Tracklist = []
        

    async def on_ready(self):
        logging.info(f'We have logged in as {bot.user} at {datetime.now()}')
        logging.debug(bot)
        
    def load_tracklist(self, path):
        with open(path) as tracklist_file:
            data = tracklist_file.read()
            self.Tracklist = fumbleboard_dbot.tracklist.Tracklist(json.loads(data))
            
    # async def list_response(ctx):
    #     response = "\n".join([f'Title:{Track.Title}' for Track in self.Tracklist.Tracks])
    #     logging.info('list function , response {}'.format(response))
    #     await ctx.send(response)
    
            
bot = Bot(command_prefix=commands.when_mentioned)

@bot.command(name='list', help='list all available tracks')
async def lister(ctx):
    response = "\n".join([f'Title:{Track.Title}' for Track in bot.Tracklist.Tracks])
    await ctx.send(response)
