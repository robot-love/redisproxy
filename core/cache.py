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
        self._lock = threading.Lock()
        self._count = 0

        if capacity <= 0:
            # todo: for capacity < 0, disable the capacity eviction policy
            raise ValueError("Capacity must be a non-negative integer.")
        self.capacity = capacity

        if ttl <= 0:
            raise ValueError("TTL must be a positive float.")
        self.ttl = ttl

    def __len__(self):
        return self._count

    def get(self, key):
        with self._lock:
            if key in self._store and not self.is_expired(key):
                self._store.move_to_end(key)
                return self._store[key].value
        return None

    def add(self, key, value):
        # todo: make this thread-safe
        with self._lock:
            self._store[key] = Entry(value, self.ttl, time())
            self._store.move_to_end(key)
            self._count += 1
        if len(self._store) > self.capacity:
            self._make_room()

    def _evict_lru(self):
        self._store.popitem(last=False)
        self._count -= 1

    def _evict_all_expired(self):
        """
        Clean up any expired cache entries. These should be evicted before we remove the least recently used entry.

        We do not have a guarantee that the LRU entry is the one that expires first. NOT thread safe.

        :return:
        """
        space_freed = False
        for key in list(self._store.keys()):
            if self.is_expired(key):
                self._store.pop(key)
                self._count -= 1
                space_freed = True
        return space_freed

    def _make_room(self):
        """
        Clean up the cache by first removing expired entries, and if that doesn't free up any stored elements, evict the
        least recently used entry.

        Thread safe.
        """
        with self._lock:
            if self._evict_all_expired():
                return
            self._evict_lru()

    def get_lru_key(self):
        return next(iter(self._store))

    def is_expired(self, key) -> bool:
        return time() > self._store[key].expiry

    def __contains__(self, item):
        return item in self._store.keys() and not self.is_expired(item)
