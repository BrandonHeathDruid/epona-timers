from enum import Enum


class BOSS_TYPE(Enum):
    OTHER = 0,
    WARDEN = 1,
    METEORIC = 2,
    FROZEN = 3,
    DL = 4,
    EDL = 5,
    RINGS = 6,
    MIDS = 6,
    EGS = 7


_t = 'type'
_r = 'respawn'
_w = 'window'

bosses = {
    'eye': {
        _t: BOSS_TYPE.FROZEN,
        _r: 30,
        _w: 0
    },
    'swampie': {
        _t: BOSS_TYPE.FROZEN,
        _r: 35,
        _w: 0
    },
    'woody': {
        _t: BOSS_TYPE.FROZEN,
        _r: 40,
        _w: 0
    },
    'chained': {
        _t: BOSS_TYPE.FROZEN,
        _r: 45,
        _w: 0
    },
    'grom': {
        _t: BOSS_TYPE.FROZEN,
        _r: 50,
        _w: 0
    },
    'pyrus': {
        _t: BOSS_TYPE.FROZEN,
        _r: 55,
        _w: 0
    },
    '155': {
        _t: BOSS_TYPE.DL,
        _r: 60,
        _w: 0
    },
    '160': {
        _t: BOSS_TYPE.DL,
        _r: 65,
        _w: 0
    },
    '165': {
        _t: BOSS_TYPE.DL,
        _r: 70,
        _w: 0
    },
    '170': {
        _t: BOSS_TYPE.DL,
        _r: 80,
        _w: 0
    },
    '180': {
        _t: BOSS_TYPE.DL,
        _r: 90,
        _w: 0
    },
    '185': {
        _t: BOSS_TYPE.EDL,
        _r: 75,
        _w: 0
    },
    '190': {
        _t: BOSS_TYPE.EDL,
        _r: 85,
        _w: 0
    },
    '195': {
        _t: BOSS_TYPE.EDL,
        _r: 95,
        _w: 0
    },
    '200': {
        _t: BOSS_TYPE.EDL,
        _r: 105,
        _w: 0
    },
    '205': {
        _t: BOSS_TYPE.EDL,
        _r: 115,
        _w: 0
    },
    '210': {
        _t: BOSS_TYPE.EDL,
        _r: 125,
        _w: 0
    },
    '215': {
        _t: BOSS_TYPE.EDL,
        _r: 135,
        _w: 0
    },
    'aggy': {
        _t: BOSS_TYPE.MIDS,
        _r: 1894,
        _w: 1894
    },
    'mord': {
        _t: BOSS_TYPE.MIDS,
        _r: 2160,
        _w: 2160
    },
    'hrung': {
        _t: BOSS_TYPE.MIDS,
        _r: 2160,
        _w: 2160
    },
    'necro': {
        _t: BOSS_TYPE.MIDS,
        _r: 2160,
        _w: 2160
    },
    'prot': {
        _t: BOSS_TYPE.EGS,
        _r: 1190,
        _w: 0
    },
    'gele': {
        _t: BOSS_TYPE.EGS,
        _r: 2880,
        _w: 2880
    },
    'bt': {
        _t: BOSS_TYPE.EGS,
        _r: 2880,
        _w: 2880
    },
    'dino': {
        _t: BOSS_TYPE.EGS,
        _r: 2880,
        _w: 2880
    },
    'east': {
        _t: BOSS_TYPE.RINGS,
        _r: 255,
        _w: 0
    },
    'north': {
        _t: BOSS_TYPE.RINGS,
        _r: 255,
        _w: 0
    },
    'south': {
        _t: BOSS_TYPE.RINGS,
        _r: 255,
        _w: 0
    },
    'center': {
        _t: BOSS_TYPE.RINGS,
        _r: 255,
        _w: 0
    }
}
