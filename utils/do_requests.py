import requests as rq
from config.environment import API_URL, MAX_ROWS


def get_request(uri, params={}):
    resp = rq.get(API_URL+uri, params=params)
    return resp.json()
