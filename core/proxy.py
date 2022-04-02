from .cache import LRUCache

import redis

# todo: make sure redis is running
# todo: make sure redis is configured correctly
# todo: make sure redis is not running on the same host/port as the proxy
# todo: pass cache and client to the proxy by dependency injection
# todo: add circuit breaker to client calls


class Proxy:
    """
    A simple proxy that caches requests to a redisserver.
    """
    def __init__(self, client, cache):
        """
        Initialize the Redis Proxy

        """
        self.client = client
        self.cache = cache
        # self.cache = LRUCache(cache_capacity, cache_expiry_time)
        # self.redis_client = redis.Redis(host=redis_ip, port=redis_port, db=0)

    def get(self, key):
        if key in self.cache:
            return self.cache.get(key)
        else:
            value = self.redis_client.get(key)
            self.cache.add(key, value)
            return value
