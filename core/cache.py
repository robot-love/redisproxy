from time import time_ns
from collections import OrderedDict


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
        self.store = OrderedDict()

        if capacity < 0:
            # todo: for capacity < 0, disable the capacity eviction policy
            raise ValueError("Capacity must be a non-negative integer.")
        self.capacity = capacity

        if ttl <= 0:
            raise ValueError("TTL must be a positive float.")
        self.ttl = ttl

    def __len__(self):
        return len(self.store)

    def get(self, key):
        if key in self.store:
            if self.is_expired(key):
                self.store.pop(key)
                return None
            else:
                self.store.move_to_end(key)
                return self.store[key].value
        else:
            return None

    def add(self, key, value):
        self.store[key] = Entry(value, self.ttl, time())
        self.store.move_to_end(key)
        if len(self.store) > self.capacity:
            # lazy eviction
            self.make_room()

    def evict_lru(self):
        self.store.popitem(last=False)

    def evict_all_expired(self):
        """
        Clean up any expired cache entries. These should be evicted before we remove the least recently used entry.

        We do not have a guarantee that the LRU entry is the one that expires first.

        :return:
        """
        space_freed = False
        for key in list(self.store.keys()):
            if self.is_expired(key):
                self.store.pop(key)
                space_freed = True
        return space_freed

    def make_room(self):
        """
        Clean up the cache by first removing expired entries, and if that doesn't free up any stored elements, evict the
        least recently used entry.

        :return:
        """
        if not self.evict_all_expired():
            self.evict_lru()

    def get_lru_key(self):
        return next(iter(self.store))

    def is_expired(self, key):
        return time() > self.store[key].expiry

    def __contains__(self, item):
        return item in self.store.keys() and not self.is_expired(item)
