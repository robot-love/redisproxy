from core.cache import LRUCache
from time import sleep


def test_lru_cache_size_limit():
    cache = LRUCache(capacity=5, ttl=5)
    for i in range(6):
        cache.add(i, i)
    assert len(cache) == 5


def test_lru_cache_evicts_least_recently_used_item():
    cache = LRUCache(capacity=3, ttl=10)
    for i in range(4):
        cache.add(i, i)
    # check capacity is respected
    assert len(cache) == 3

    # check expected elements are in cache
    assert cache.get(0) == None
    assert cache.get(1) == 1
    assert cache.get(2) == 2
    assert cache.get(3) == 3

    # access an item to update its timestamp
    assert cache.get(1) == 1

    # lru item should now be '2
    cache.add(4, 4)
    assert cache.get(2) is None


def test_lru_cache_does_not_return_expired_entries():
    cache = LRUCache(capacity=5, ttl=0.01)
    for i in range(5):
        cache.add(i, i)
    assert len(cache) == 5
    assert cache.get(0) == 0
    assert cache.get(1) == 1
    assert cache.get(2) == 2
    assert cache.get(3) == 3
    assert cache.get(4) == 4

    sleep(0.02)
    assert cache.get(0) is None
    assert cache.get(1) is None
    assert cache.get(2) is None
    assert cache.get(3) is None
    assert cache.get(4) is None
    assert len(cache) == 5 # cache entries are expired, but still in cache


def test_lru_cache_evicts_expired_entries_before_least_recently_used_entries():
    cache = LRUCache(capacity=2, ttl=0.1)
    cache.add(0, 0)
    sleep(0.06)
    cache.add(1, 1)
    # make `1` the lru
    cache.get(0)
    # expire `0`
    sleep(0.06)
    assert cache._is_expired(0)
    # reach capacity
    cache.add(2, 2)
    assert cache.get(0) is None
    assert cache.get(1) == 1
    assert cache.get(2) == 2


def test_lru_cache_get_correct_lru_entry():
    cache = LRUCache(capacity=4, ttl=2)
    for i in range(4):
        cache.add(i, i)
    assert cache._get_lru_key() == 0


def test_lru_cache_get_correct_lru_entry_after_eviction():
    cache = LRUCache(capacity=4, ttl=2)
    for i in range(4):
        cache.add(i, i)
    cache.add(4, 4)
    assert cache.get(0) is None
    assert cache._get_lru_key() == 1


def test_lru_cache_evict_all_expired_removes_all_expired_entries():
    cache = LRUCache(capacity=4, ttl=0.1)
    for i in range(4):
        cache.add(i, i)
    sleep(0.2)
    assert cache._evict_all_expired() is True
    assert len(cache) == 0
