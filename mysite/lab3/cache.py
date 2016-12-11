from redis import StrictRedis
from bson.json_util import dumps, loads


cache = StrictRedis()


def get_from(query):
    return loads(cache.get(query).decode('utf8'))


def is_key_present(key):
    return cache.get(key) is not None


def set_from(query, results):

    for item in results:
        print item
    flights = []
    for item in results:
        flights.append(item)
    cache.set(query, dumps(flights))