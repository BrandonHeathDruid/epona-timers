from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    message: str


class BossData(BaseModel):
    name: str
    type: str
    respawn: int
    window: int


class BossTimer(BaseModel):
    name: str
    timer: datetime | None