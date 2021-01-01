import argparse
import logging
import sys
from dotenv import load_dotenv
import os
from fumbleboard_dbot.bot import FumbleBoardBot
#from fumbleboard_dbot.tracklist import Tracklist

import itertools

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
logging.info(f'Setting LOGLEVEL={loglevel} ({numeric_level})')

#################################
# load config
load_dotenv()
bot_token = os.getenv('DISCORD_BOT_TOKEN')


# taglist = list(sorted(set(list(itertools.chain(*[el['Tags'] for el in playlist])))))
# tagdict = {t:list(filter(lambda a: '80s' in a['Tags'], playlist)) for t in  taglist}



########################################
# configure and run the bot
fbbot = FumbleBoardBot(conf_url = ("file:///" + os.getcwd() + "/config.json"))
fbbot.run(bot_token)