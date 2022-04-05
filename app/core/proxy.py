from core.cache import LRUCache

import redis
import aioredis
from typing import Awaitable

class Proxy:
    """
    A simple proxy.
    """
    def __init__(self, client, cache):
        """
        Initialize the proxy.

        :param client: The client to use for the proxy. Must support a get() method.
        :param cache: The cache to use for the proxy. Must support a get() and add() method.
        """
        self.client = client
        self.cache = cache

    async def get(self, key):
        # todo: handle unavailable client
        if key in self.cache:
            return self.cache.get(key)
        else:
            value = self.client.get(key)
            if value:
                self.cache.add(key, value)
            return value


def redis_proxy_factory(redis_host, redis_port, cache_capacity, cache_ttl):
    """
    Create a proxy for a Redis client.

    :param redis_host: hostname or ip for the backing Redis instance
    :param redis_port: port for the backing Redis instance
    :param cache_capacity: maximum number of items to cache
    :param cache_ttl: expiry time for cached items in seconds
    :return: Proxy object with an LRU cache and a redis client connection
    """
    client = redis.Redis(host=redis_host, port=redis_port)
    cache = LRUCache(capacity=cache_capacity, ttl=cache_ttl)
    return Proxy(client, cache)


def aio_redis_proxy_factory(redis_host, redis_port, cache_capacity, cache_ttl):
    """
    Create an async proxy for a Redis client.

    :param redis_host: hostname or ip for the backing Redis instance
    :param redis_port: port for the backing Redis instance
    :param cache_capacity: maximum number of items to cache
    :param cache_ttl: expiry time for cached items in seconds
    :return: Proxy object with an LRU cache and a redis client connection
    """
    client = aioredis.from_url(f"redis://{redis_host}:{redis_port}")
    cache = LRUCache(capacity=cache_capacity, ttl=cache_ttl)
    return Proxy(client, cache)