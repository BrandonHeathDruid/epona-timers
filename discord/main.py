import os
import sys

_path_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


import discord
import threading
import keep_alive
import logging
import pymongo
import certifi
import json
from datetime import datetime, timedelta

logging.basicConfig(format='%(levelname)s %(asctime)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def get_dhm(array_values):
    days = 0
    hours = 0
    minutes = 0
    for value in array_values:
        if len(value) > 1:
            if value[-1] == 'd':
                days = int(value[:-1])
            elif value[-1] == 'h':
                hours = int(value[:-1])
            elif value[-1] == 'm':
                minutes = int(value[:-1])
            else:
                raise ValueError
        else:
            raise ValueError

    return days, hours, minutes


class DiscordBot(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
  
        self._bosses_data_f = _path_parent + '/api/static/bosses_data.json'
        logger.info(f'Loading bosses data from: {self._bosses_data_f}')
        with open(self._bosses_data_f) as f:
            self.bosses_data = json.load(f)
            self.boss_names = self.bosses_data.keys()
            logger.info(f'Loaded {len(self.boss_names)} bosses')
  
        self.db = pymongo.MongoClient(os.getenv("URL_MONGODB"), tlsCAFile=certifi.where())[os.getenv('DB_NAME')]
  
  
    def set_timer(self, name, timer):
        self.db.timer.update_one({'name': name}, {'$set': {'timer': timer}}, upsert=True)
      
    
    async def on_ready(self):
        logger.info('Logged')
    
    
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return
    
        logger.info(message.content)
        action = None
        cmd, *args = message.content.lower().split(' ')
        len_args = len(args)
        
        if cmd in self.boss_names:  # can use bisect to have better performance, but the dataset is small
            boss = cmd
            boss_timer_minutes = self.bosses_data[boss]['respawn']
            next_respawn = datetime.utcnow() + timedelta(minutes=boss_timer_minutes)
            self.set_timer(boss, next_respawn)
            action = 'timed'
        elif cmd == 'set' and len_args > 1 and args[0] in self.boss_names:
            try:
                days, hours, minutes = get_dhm(args[1:])  
                next_respawn = datetime.utcnow() + timedelta(days=days, hours=hours, minutes=minutes)
                self.set_timer(args[0], next_respawn)
                action = f'set {days} {hours} {minutes}'
            except ValueError:
                pass 
        elif cmd == 'reset' and len_args == 1 and args[0] in self.boss_names:
            self.set_timer(args[0], None)
            action = 'reset'

        logger.info(f'Action: {action}')

        
threading.Thread(target=keep_alive.run, daemon=True).start()

client = DiscordBot(intents=discord.Intents.all(), status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.playing, name='reading'))
client.run(os.getenv('TOKEN'))
