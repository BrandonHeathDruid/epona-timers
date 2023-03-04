import os

_path_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import discord
import threading
import keep_alive
import logging
import pymongo
import certifi
import json
from datetime import datetime, timedelta
import bisect

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

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

        self._bosses_data_f = _path_parent + '/api/static/bosses.json'
        logger.info(f'Loading bosses data from: {self._bosses_data_f}')
        with open(self._bosses_data_f) as f:
            self.bosses_data = sorted(json.load(f), key=lambda x: x['name'])
            self.bosses_names = [b['name'] for b in self.bosses_data]
            self.len_bosses_names = len(self.bosses_names)
            logger.info(f'Loaded {self.len_bosses_names} bosses')

        self.db = pymongo.MongoClient(
            os.getenv("URL_MONGODB"),
            tlsCAFile=certifi.where())[os.getenv('DB_NAME')]
        
        self.influx_org = os.getenv("ORG_INFLUXDB")
        self.influx_client = InfluxDBClient(url=os.getenv("URL_INFLUXDB"),
                                            token=os.getenv("TOKEN_INFLUXDB"),
                                            org=self.influx_org)
        self.influx_write = self.influx_client.write_api(
            write_options=WriteOptions(write_type=SYNCHRONOUS))
        self.influx_bucket = os.getenv("BUCKET_INFLUXDB")

    def check_boss_exists(self, boss):
        index = bisect.bisect_left(self.bosses_names, boss)
        if index < self.len_bosses_names and self.bosses_names[index] == boss:
            return index

    def set_timer(self, boss_data, timer: datetime, influx_timer=None):
        logger.info(boss_data)
        self.db.timer.update_one({'name': boss_data['name']}, {'$set': {
            'timer': timer
        }},
                                 upsert=True)

        
        if timer is not None:
            point = Point('timer').tag('server', 'Epona').field('type', boss_data['type'])
            point = point.field('name', boss_data['name'])
            if influx_timer is not None:
                point.time(influx_timer)
            self.influx_write.write(self.influx_bucket, self.influx_org, point)

    async def on_ready(self):
        logger.info('Logged')

    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return

        logger.info(message.content)
        action = None
        cmd, *args = message.content.lower().split(' ')
        len_args = len(args)

        boss_index = self.check_boss_exists(cmd)

        if boss_index is not None:
            boss = self.bosses_data[boss_index]
            boss_timer_minutes = boss['respawn']
            next_respawn = datetime.utcnow() + timedelta(
                minutes=boss_timer_minutes)
            self.set_timer(boss, next_respawn, action)
            action = 'timed'
        elif cmd == 'set' and len_args > 1:
            boss_index = self.check_boss_exists(args[0])
            if boss_index is not None:
                try:
                    days, hours, minutes = get_dhm(args[1:])
                    next_respawn = datetime.utcnow() + timedelta(
                        days=days, hours=hours, minutes=minutes)

                    influx_timer = next_respawn - timedelta(minutes=self.bosses_data[boss_index]['respawn'])
                    
                    self.set_timer(self.bosses_data[boss_index], next_respawn, influx_timer)
                    action = f'set {days} {hours} {minutes}'
                except ValueError:
                    pass
        elif cmd == 'reset' and len_args == 1:
            boss_index = self.check_boss_exists(args[0])
            if boss_index is not None:
                self.set_timer(self.bosses_data[boss_index], None)
                action = 'reset'

        logger.info(f'Action: {action}')


threading.Thread(target=keep_alive.run, daemon=True).start()

client = DiscordBot(intents=discord.Intents.all(),
                    status=discord.Status.online,
                    activity=discord.Activity(
                        type=discord.ActivityType.playing, name='reading'))
client.run(os.getenv('TOKEN'))
