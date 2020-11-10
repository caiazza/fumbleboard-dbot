from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
import json
import random
from datetime import datetime

load_dotenv()
bot_token = os.getenv('DISCORD_BOT_TOKEN')

bot = commands.Bot(command_prefix=commands.when_mentioned)

# read the playlist
with open("playlist.json") as playlist_file:
    data = playlist_file.read()
    playlist = json.loads(data)['songs']

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user} at {datetime.now()}')

@bot.command(name='random', help='get a random song')
async def randomize(ctx):
    response = random.choice([f'title:{el["title"]} , author: {el["author"]}' for el in playlist])
    await ctx.send(response)

@bot.command(name='list', help='list all available songs')
async def lister(ctx):
    response = "\n".join([f'title:{el["title"]} , author: {el["author"]}' for el in playlist])
    await ctx.send(response)

@bot.command(name='time', help='print current time')
async def timer(ctx):
    response = f'Hi {ctx.message.author.mention} it is {datetime.now()}'
    await ctx.send(response)

bot.run(bot_token)
