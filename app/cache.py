from datetime import datetime, timedelta

class Entry:
    def __init__(self, value, ttl):
        self.value = value
        self.created = datetime.now()
        self.expiry = self.created + timedelta(seconds=ttl)
        # I'm not a big fan of maintaining invariance through another object, particularly in a language where I can't
        # declare private member variables or friend classes, but really, I think it's the simplest way.
        self.last_accessed = self.created

    def is_expired(self):
        return datetime.now() >= self.expiry

    # this one was mainly for debug purposes
    def __repr__(self):
        return self.value


class LRUCache:
    capacity: int
    cache: dict
    ttl: int

    def __init__(self, capacity: int, ttl: int):
        self.cache = dict()
        if capacity < 0:
            raise ValueError("Capacity must be a non-negative integer.")
        if ttl < 0:
            raise ValueError("TTL must be a non-negative integer.")
        self.capacity = capacity
        self.ttl = ttl

    def get(self, key):
        if key in self.cache.keys and not self.cache[key].is_expired():
            self.cache[key].last_accessed = datetime.now()
            return self.cache[key].value
        else:
            return None

    def add(self, key, value):
        self.cache[key] = Entry(value, self.ttl)
        if len(self.cache) > self.capacity:
            self.evict_lru()

    def evict_lru(self):
        self.cache.pop(self.find_lru_key())

    def find_lru_key(self):
        # O(n)
        return min(self.cache, key=lambda x: self.cache[x].last_accessed)

    def __contains__(self, item):
        return item in self.cache.keys() and not self.cache[item].is_expired()