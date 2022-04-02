from core.proxy import Proxy
from core.cache import LRUCache

import redis
from aiohttp import web
import yaml

# todo: add logging
# todo: add circuit breaker
# todo: add metrics

def load_config(config_file):
    # todo: validate config
    with open(config_file) as f:
        return yaml.load(f)


def redis_proxy_factory(redis_host, redis_port, cache_capacity, cache_ttl):
    client = redis.Redis(host=redis_host, port=redis_port, db=0)
    cache = LRUCache(capacity=cache_capacity, ttl=cache_ttl)
    return Proxy(client, cache)


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    try:
        result = await proxy.get(name)
    except ConnectionError:
        return web.Response(text="Proxy server is down", status=500)
    except Exception:
        return web.Response(text="Proxy server is down", status=500)
    if not result:
        return web.Response(text="Key not found", status=404)
    return web.Response(text=result)


if __name__ == '__main__':
    global proxy

    proxy = redis_proxy_factory('localhost', 5000, 20, 10)
    app = web.Application()
    app.router.add_get('/', handle)

    web.run_app(app)