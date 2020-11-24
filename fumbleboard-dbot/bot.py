from discord.ext import commands
import discord
import json
import random
from datetime import datetime
# import youtube_dl
import time
import itertools



#################################
# instantiate the bot
# bot = commands.Bot(command_prefix=commands.when_mentioned)

#################################
# read the playlist
with open("playlist.json") as playlist_file:
    data = playlist_file.read()
    playlist = json.loads(data)

taglist = list(sorted(set(list(itertools.chain(*[el['Tags'] for el in playlist])))))
tagdict = {t:list(filter(lambda a: '80s' in a['Tags'], playlist)) for t in  taglist}

logging.info('Loaded playlist with {} songs'.format(len(playlist)))

# [python - Discord.py rewrite and youtube_dl - Stack Overflow](https://stackoverflow.com/questions/60241517/discord-py-rewrite-and-youtube-dl)
# Suppress noise about console usage from errors

# youtube_dl.utils.bug_reports_message = lambda: ''

# ytdl_format_options = {
#     'format': 'bestaudio/best',
#     'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
#     'restrictfilenames': True,
#     'noplaylist': False,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
# }

# ffmpeg_options = {
#     'options': '-vn'
# }

# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)

#         self.data = data

#         self.title = data.get('title')
#         self.url = data.get('url')

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]

#         filename = data['url'] if stream else ytdl.prepare_filename(data)
#         return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

#################################
# bot functions 

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user} at {datetime.now()}')
    logging.info(f'We have logged in as {bot.user} at {datetime.now()}')
    logging.debug(bot)

@bot.command(name='random', help='get a random song')
async def randomize(ctx):
    response = random.choice([f'Artist: {el["Artist"]}, Title:{el["Title"]} , Tags: {",".join(el["Tags"])}' for el in playlist])
    logging.info('random function , response {}'.format(response))
    await ctx.send(response)

@bot.command(name='list', help='list all available songs')
async def lister(ctx):
    response = "\n".join([f'Artist: {el["Artist"]}, Title:{el["Title"]} ,Tags: {",".join(el["Tags"])}' for el in playlist])
    logging.info('lister function , response {}'.format(response))
    await ctx.send(response)

@bot.command(name='tags', help='list all available tags')
async def tags(ctx):
    response = '\n'.join([f'{k} : {len(v)} songs' for k,v in tagdict.items()])
    logging.info('listtag function , response {}'.format(response))
    await ctx.send(response)

@bot.command(name='tagls', help='list songs in atag')
async def tagls(ctx, *tagname):
    if tagname is not None and len(tagname) ==1 :
        response = "\n".join([f'Artist: {el["Artist"]}, Title:{el["Title"]}' for el in tagdict[tagname[0]]])
        logging.info('listtag function , response {}'.format(response))
        await ctx.send(response)
    else:
        response = f'Hi {ctx.message.author.mention}, you forgot to give a tag!\n Use the command like \n tagls TAG'
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

# @bot.command()
# async def streamyt(ctx, *, urlm ,help='stream an youtube channel, "streamyt URL"'):
#     """Streams from a url (same as yt, but doesn't predownload)"""
#     player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
#     ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
#     await ctx.send('Now playing: {}'.format(player.Title))

@bot.command(name="playlocal")
async def playlocal(ctx, *args):
    # Gets voice channel of message author
    voice_channel = ctx.author.voice
    # channel = None
    print(args)
    if voice_channel != None:
        channel = voice_channel.channel.name
        vc = await voice_channel.channel.connect()
        print(voice_channel)
        try :
            vc.play(discord.FFmpegPCMAudio(source="/home/kidpixo/music/beets/Cowboy Bebop/Cowboy Bebop/00 Bad dog no biscuits.mp3"))
            # Sleep while audio is playing.
            while vc.is_playing():
                time.sleep(.1)
            await vc.disconnect()
        except discord.errors.Forbidden:
            log.error('Cannot play audio file.')
    else:
        await ctx.send(str(ctx.author.name) + " you are note not in a voice channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()

# bot.run(bot_token)
