from cache import LRUCache

import redis
# from http.server import HTTPServer


class RedisProxy:
    cache: LRUCache
    ip: str
    port: str

    def __init__(self, redis_ip, redis_port, cache_capacity, cache_expiry_time):
        """
        Initialize the Redis Proxy

        :param redis_ip: the ip of the redis server
        :param redis_port: redis server port
        :param cache_capacity: max number of keys the cache can hold
        :param cache_expiry_time: Expiry time of a cache entry in seconds
        """
        self.cache = LRUCache(cache_capacity, cache_expiry_time)
        self.redis_client = redis.Redis(host=redis_ip, port=redis_port, db=0)

    def get(self, key):
        if key in self.cache:
            return self.cache.get(key)
        else:
            value = self.redis_client.get(key)
            self.cache.add(key, value)
            return value
