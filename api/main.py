import os

_path_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Query, Path, HTTPException
from fastapi.responses import RedirectResponse
from models import Message, BossData, BossTimer
import uvicorn
from uvicorn.config import LOGGING_CONFIG
import pymongo
import certifi
import json
import logging
import bisect

logging_fmt = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(format=logging_fmt, level=logging.INFO)
LOGGING_CONFIG['formatters']['default']['fmt'] = logging_fmt
LOGGING_CONFIG['formatters']['access'][
    'fmt'] = '%(levelprefix)s %(asctime)s - "%(request_line)s" %(status_code)s'

db = pymongo.MongoClient(os.getenv('URL_MONGODB'),
                         tlsCAFile=certifi.where())[os.getenv('DB_NAME')]

with open(_path_parent + '/api/static/bosses.json') as f:
    bosses_data = sorted(json.load(f), key=lambda x: x['name'])
    bosses_names = [b['name'] for b in bosses_data]
    len_bosses_names = len(bosses_names)


def check_boss_exists(boss):
    index = bisect.bisect_left(bosses_names, boss)
    if index < len_bosses_names and bosses_names[index] == boss:
        return index


app = FastAPI()


@app.get('/health', summary='Get server health')
def health():
    return {'status': 'OK'}


@app.get('/',
         response_class=RedirectResponse,
         status_code=302,
         summary='Redirect to the docs')
def home():
    return '/docs'


@app.get('/v1/boss/{boss}',
         response_model=BossData,
         responses={
             404: {
                 "model": Message,
                 "description": "The boss was not found"
             }
         },
         tags=['BossData'],
         summary='Get boss data')
def boss_boss(boss: str = Path(description="boss' name", example=180)):
    index = check_boss_exists(boss)
    if index is not None:
        return bosses_data[index]

    raise HTTPException(status_code=404, detail='BossData not found')


@app.get('/v1/bosses',
         response_model=list[BossData],
         tags=['BossData'],
         summary='Get all bosses data')
def bosses():
    return bosses_data


@app.get('/v1/timer/{boss}',
         response_model=BossTimer,
         responses={
             404: {
                 "model": Message,
                 "description": "The boss was not found"
             }
         },
         tags=['BossTimer'],
         summary='Get boss timer')
def timer_boss(boss: str = Path(default=None,
                                description="boss' name",
                                example=180)):
    if check_boss_exists(boss) is not None:
        boss_timer = db.timer.find_one({'name': boss}, {'_id': 0})
        if boss_timer is not None:
            return boss_timer

    raise HTTPException(status_code=404, detail='BossTimer not found')


@app.get('/v1/timers',
         response_model=list[BossTimer],
         tags=['BossTimer'],
         summary='Get specific bosses timer')
def timers(b: list[str] | None = Query(default=[], example=['180', 'prot'])):
    valid_bosses = []
    for boss in b:
        index = check_boss_exists(boss)
        if index is not None:
            valid_bosses.append(boss)

    return list(db.timer.find({'name': {'$in': valid_bosses}}, {'_id': 0}))


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080)
