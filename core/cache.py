from datetime import datetime, timedelta


class Entry:
    """
    A cache entry.
    """
    def __init__(self, value, ttl):
        self.value = value
        self.created = datetime.now()
        self.expiry = self.created + timedelta(seconds=ttl)

    def __repr__(self):
        return self.value


class LRUCache:
    """
    A least-recently-used cache.
    """
    capacity: int
    cache: dict
    ttl: int

    def __init__(self, capacity: int, ttl: int):
        self.cache = dict()
        self.last_accessed = dict()
        if capacity < 0:
            # todo: for capacity < 0, disable the eviction policy
            raise ValueError("Capacity must be a non-negative integer.")
        if ttl < 0:
            raise ValueError("TTL must be a non-negative integer.")
        self.capacity = capacity
        self.ttl = ttl

    def get(self, key):
        if key in self.cache and not self.is_expired(key):
            self.update_access_time(key)
            return self.cache[key].value
        else:
            return None

    def add(self, key, value):
        self.cache[key] = Entry(value, self.ttl)
        self.update_access_time(key)
        if len(self.cache) > self.capacity:
            print("Evicting LRU")
            self.evict_lru()

    def update_access_time(self, key):
        self.last_accessed.update({key: datetime.now()})

    def evict_lru(self):
        self.cache.pop(self.find_lru_key())

    def find_lru_key(self):
        # O(n)
        return min(self.cache, key=lambda x: self.last_accessed[x].last_accessed)

    def is_expired(self, key):
        return self.last_accessed[key] > self.cache[key].expiry

    def __contains__(self, item):
        return item in self.cache.keys() and not self.is_expired(item)
