from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
import json
import random
from datetime import datetime
import logging
import sys
import argparse
import youtube_dl
import time

#################################
# parse logging level from cli
parser = argparse.ArgumentParser()
parser.add_argument("-log", "--log", nargs='+', help="Provide logging level. Example --log debug'")

loglevel = parser.parse_args(None).log
# set standard logging to INFO
loglevel = loglevel[0] if loglevel else 'INFO'
numeric_level = getattr(logging, loglevel.upper())
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)

#################################
# instantiate logger to stdout
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=numeric_level, format=FORMAT,stream=sys.stdout)
logging.info('Setting LOGLEVEL={} ({})'.format(loglevel,numeric_level))

#################################
# load config
load_dotenv()
bot_token = os.getenv('DISCORD_BOT_TOKEN')

#################################
# instantiate the bot
bot = commands.Bot(command_prefix=commands.when_mentioned)

#################################
# read the playlist
with open("playlist.json") as playlist_file:
    data = playlist_file.read()
    playlist = json.loads(data)['songs']
logging.info('Loaded playlist with {} songs'.format(len(playlist)))

# [python - Discord.py rewrite and youtube_dl - Stack Overflow](https://stackoverflow.com/questions/60241517/discord-py-rewrite-and-youtube-dl)
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

#################################
# bot functions 

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user} at {datetime.now()}')
    logging.info(f'We have logged in as {bot.user} at {datetime.now()}')
    logging.debug(bot)

@bot.command(name='random', help='get a random song')
async def randomize(ctx):
    response = random.choice([f'title:{el["title"]} , author: {el["author"]}' for el in playlist])
    logging.info('random function , response {}'.format(response))
    await ctx.send(response)

@bot.command(name='list', help='list all available songs')
async def lister(ctx):
    response = "\n".join([f'title:{el["title"]} , author: {el["author"]}' for el in playlist])
    logging.info('lister function , response {}'.format(response))
    await ctx.send(response)

@bot.command(name='time', help='print current time')
async def timer(ctx):
    response = f'Hi {ctx.message.author.mention} it is {datetime.now()}'
    logging.info('timer function , response {}'.format(response))
    await ctx.send(response)

@bot.command()
async def join(ctx):
    # channel = bot.get_channel('615140999374831641')
    channel = ctx.author.voice.channel
    logging.info('joining voice channel {}'.format(channel))
    await channel.connect()
@bot.command()
async def leave(ctx):
    # channel = bot.get_channel('615140999374831641')
    # channel = ctx.author.voice.channel
    logging.info('leaveing voice channel {}')
    await ctx.voice_client.disconnect()

@bot.command()
async def streamyt(ctx, *, urlm ,help='stream an youtube channel, "streamyt URL"'):
    """Streams from a url (same as yt, but doesn't predownload)"""
    player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send('Now playing: {}'.format(player.title))

@bot.command(name="playlocal")
async def playlocal(ctx):
    # Gets voice channel of message author
    voice_channel = ctx.author.voice.channel
    channel = None
    if voice_channel != None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(source="/home/kidpixo/music/beets/Cowboy Bebop/Cowboy Bebop/00 Bad dog no biscuits.mp3"))
        # Sleep while audio is playing.
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()

bot.run(bot_token)
