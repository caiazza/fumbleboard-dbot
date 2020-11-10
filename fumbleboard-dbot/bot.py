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

bot.run(bot_token)
