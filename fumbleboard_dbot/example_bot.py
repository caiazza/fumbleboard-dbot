import discord
import os
from dotenv import load_dotenv
import json

load_dotenv()
bot_token = os.getenv('DISCORD_BOT_TOKEN')
client = discord.Client()

# read the playlist
with open("playlist.json") as playlist_file:
    data = playlist_file.read()
    playlist = json.loads(data)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$list'):
        await message.channel.send(f'Songs : {playlist}')

client.run(bot_token)
