import os

_path_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from uvicorn.config import LOGGING_CONFIG
import pymongo
import certifi
import json
import logging
import bisect


logging_fmt = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(format=logging_fmt,
                    level=logging.INFO)
LOGGING_CONFIG["formatters"]["default"]["fmt"] = logging_fmt
LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(levelprefix)s %(asctime)s - "%(request_line)s" %(status_code)s'

db = pymongo.MongoClient(os.getenv("URL_MONGODB"), tlsCAFile=certifi.where())[os.getenv('DB_NAME')]

with open(_path_parent + '/api/static/bosses.json') as f:
    bosses_data = sorted(json.load(f), key=lambda x: x['name'])
    bosses_names = [b['name'] for b in bosses_data]
    len_bosses_names = len(bosses_names)       

app = FastAPI()


def check_boss_exists(boss):
    index = bisect.bisect_left(bosses_names, boss)
    if index < len_bosses_names and bosses_names[index] == boss:
        return index


@app.get('/health')
def ping():
    return {'status': 'OK'}
    

@app.get('/', response_class=RedirectResponse, status_code=302)
def home():
    return '/docs'


@app.get('/v1/bosses')
def bosses():
    return bosses_data


@app.get('/v1/boss/{boss}')
def boss_boss(boss: str):
    index = check_boss_exists(boss)
    if index is not None:
        return bosses_data[index]


@app.get('/v1/timer/{boss}')
def timer_boss(boss: str):
    if check_boss_exists(boss) is not None:
        return db.timer.find_one({'name': boss}, {'_id': 0})



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080) 