import discord
from discord.ext import commands
import logging
from datetime import datetime
import fumbleboard_dbot.tracklist
# from fumbleboard_dbot.tracklist import Tracklist
import json
import urllib

__all__ = ("FumbleBoardBot")

class FumbleBoardBot(commands.Bot):
    """
    The fumble board bot basic definition
    """
    
    def __init__(self, *args, conf_url, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned,*args, **kwargs)
        data = urllib.request.urlopen(url = conf_url)
        self.Tracklist = []
        self.command(name='list', help='list all available tracks')(self.list_response)
        self.command(name='play', help='starts reproducing a playlist in the vocal channel')(self.play_single_track)

    async def on_ready(self):
        logging.info(f'We have logged in as {self.user} at {datetime.now()}')
        logging.debug(self)
        
    def load_tracklist(self, path):
        with open(path) as tracklist_file:
            data = tracklist_file.read()
            self.Tracklist = fumbleboard_dbot.tracklist.Tracklist(json.loads(data))
   
    # @commands.Bot.command(name='list', help='list all available tracks')
    # @self.command(name='list', help='list all available tracks')
    async def list_response(self, ctx, arg):
        response = "\n".join([f'Title:{Track.Title}' for Track in self.Tracklist.Tracks])
        logging.info('list function , response {}'.format(response))
        await ctx.send(response)
        
    async def play_single_track(self, ctx, Track: fumbleboard_dbot.tracklist.Track):
        await ctx.send(Track)
    
            

# @fbbot.command(name='list', help='list all available tracks')
# async def lister(ctx):
#     await ctx.send(len(fbbot.Tracklist))
    # await fbbot.list_response(ctx)
    # response = "\n".join([f'Title:{Track.Title}' for Track in fbbot.Tracklist.Tracks])
    # await ctx.send(response)
