import os

_path_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
import uvicorn
import pymongo
import certifi
import json

db = pymongo.MongoClient(os.getenv("URL_MONGODB"), tlsCAFile=certifi.where())[os.getenv('DB_NAME')]

with open(_path_parent + '/api/static/bosses.json') as f:
    bosses_data = json.load(f)


app = FastAPI()


@app.get('/health')
def ping():
    return 'OK'


@app.get('/')
def home():
    return list(db.timer.find({}, {'_id': 0}))


@app.get('/bosses')
def bosses():
    return bosses_data


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080) 