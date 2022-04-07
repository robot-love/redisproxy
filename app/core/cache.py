from time import time_ns
from collections import OrderedDict
import threading


def time():
    return time_ns() / (10 ** 9)


class Entry:
    """
    A simple cache entry.
    """
    def __init__(self, value, ttl, created_time):
        self.value = value
        self.created = created_time
        self.expiry = self.created + ttl

    def __repr__(self):
        return f"<Entry: {self.value}>"


class LRUCache:
    """
    A simple cache with a least-recently-used eviction policy.
    """

    def __init__(self, capacity: int, ttl: float):
        self._store = OrderedDict()

        if capacity <= 0:
            # todo: for capacity < 0, disable the capacity eviction policy
            raise ValueError("Capacity must be a non-negative integer.")
        self.capacity = capacity

        if ttl <= 0:
            raise ValueError("TTL must be a positive float.")
        self.ttl = ttl

    def __len__(self):
        return len(self._store)

    def get(self, key):
        if key in self._store and not self._is_expired(key):
            self._store.move_to_end(key)
            return self._store[key].value

    def add(self, key, value):
        self._store[key] = Entry(value, self.ttl, time())
        self._store.move_to_end(key)
        if len(self._store) > self.capacity:
            self._evict_lru()

    def _evict_lru(self):
        self._store.popitem(last=False)

    def _get_lru_key(self):
        return next(iter(self._store))

    def _is_expired(self, key) -> bool:
        return time() > self._store[key].expiry

    def __contains__(self, item):
        return item in self._store.keys() and not self._is_expired(item)
