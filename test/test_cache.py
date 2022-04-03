from core.cache import LRUCache
from time import sleep
from pprint import pprint

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
    cache.get(1) == 1

    # lru item should now be '2
    cache.add(4, 4)
    assert cache.get(2) == None



# def test_lru_cache_does_not_return_expired_entries():
#     cache = LRUCache(capacity=5, ttl=5)
#     for i in range(5):
#         cache.add(i, i)
#     assert len(cache) == 5
#     assert cache.get(0) == 0
#     assert cache.get(1) == 1
#     assert cache.get(2) == 2
#     assert cache.get(3) == 3
#     assert cache.get(4) == 4
#
#     sleep(6)
#     assert cache.get(0) == None
#     assert cache.get(1) == None
#     assert cache.get(2) == None
#     assert cache.get(3) == None
#     assert cache.get(4) == None
#
#
# def test_lru_cache_evicts_expired_entries_before_least_recently_used_entries():
#     pass


