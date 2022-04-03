from core.proxy import Proxy


class FakeClient:
    def __init__(self, data=dict()):
        self.store = data

    def get(self, key):
        if key in self.store:
            return self.store[key]
        else:
            return None


class FakeCache:
    def __init__(self, data=dict()):
        self.store = data

    def get(self, key):
        if key in self.store:
            return self.store[key]
        else:
            return None

    def add(self, key, value):
        self.store[key] = value


def fake_redis_proxy_factory(cache_capacity, cache_ttl, fake_data = dict()):
    """
    Create a proxy for a fake Redis client.

    :param cache_capacity: maximum number of items to cache
    :param cache_ttl: expiry time for cached items in seconds
    :return: Proxy object with an LRU cache and a fake redis client connection
    """

    client = FakeClient(fake_data)
    cache = FakeCache(capacity=cache_capacity, ttl=cache_ttl)
    return Proxy(client, cache)


def test_proxy_get_request_is_cached():
    pass


