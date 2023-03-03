import discord
import os
import threading
from .. import keep_alive, bossesData
import logging
import pymongo

logging.basicConfig(format='%(levelname)s %(asctime)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    logger.info('Logged')


@client.event
async def on_message(message):
    if message.author.bot or message.guild is None:
        return

    logger.info(message.content)
    cmd, *args = message.content.lower().split(' ')
    if cmd == 'set':
        pass
    elif cmd == 'reset':
        pass
    elif cmd in ['help', 'bosslist']:
        pass
    else:
        pass

        

        


threading.Thread(target=keep_alive.run, daemon=True).start()

client.run(os.getenv("TOKEN"))
