from core.proxy import redis_proxy_factory, fake_redis_proxy_factory
from core.cache import LRUCache

from aiohttp import web
import yaml

# todo: add logging
# todo: add metrics

# todo: make sure redis is running
# todo: make sure redis is configured correctly
# todo: make sure redis is not running on the same host/port as the proxy
# todo: add circuit breaker to client calls

routes = web.RouteTableDef()


def load_config(config_file):
    # todo: validate config
    with open(config_file) as f:
        return yaml.load(f)


@routes.get('/{key}')
async def handle(request):
    key = request.match_info['key']
    try:
        print(f"Looking for: {key}")
        result = await proxy.get(key)
    except ConnectionError:
        return web.Response(text="Proxy server is down", status=500)
    except Exception as e:
        return web.Response(text=f"Unknown error: {e}", status=500)
    if not result:
        return web.Response(text="Key not found", status=404)
    return web.Response(text=result)


if __name__ == '__main__':
    global proxy

    # proxy = redis_proxy_factory('localhost', 5000, 20, 10)
    proxy = fake_redis_proxy_factory(20, 10)
    app = web.Application()
    app.router.add_get('/{key}', handle)

    web.run_app(app)