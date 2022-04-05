import pytest

from core.proxy import Proxy


class FakeClient:
    def __init__(self, data=dict()):
        self.store = data

    def get(self, key):
        if key in self.store:
            return self.store[key]
        else:
            return None


class FakeCache:
    def __init__(self, data=dict()):
        self._store = data

    def __contains__(self, item):
        return item in self._store

    def get(self, key):
        if key in self._store:
            return self._store[key]
        else:
            return None

    def add(self, key, value):
        self._store[key] = value


@pytest.fixture
def fake_proxy():
    """
    Create a proxy for a fake Redis client.

    :param cache_capacity: maximum number of items to cache
    :param cache_ttl: expiry time for cached items in seconds
    :return: Proxy object with an LRU cache and a fake redis client connection
    """
    fake_data = {
        "date": "2018-01-01",
        "time": "12:00:00",
        "price": "1.00",
        "currency": "USD"
    }

    client = FakeClient(fake_data)
    cache = FakeCache()
    return Proxy(client, cache)


@pytest.mark.asyncio
async def test_proxy_get_request_is_cached(fake_proxy):
    assert "date" not in fake_proxy.cache._store
    assert "2018-01-01" == await fake_proxy.get("date")
    assert fake_proxy.cache._store["date"] == "2018-01-01"



