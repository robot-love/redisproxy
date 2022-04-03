import redis.exceptions

from core.proxy import redis_proxy_factory
from core.cache import LRUCache
import traceback
import sys

import yaml
import argparse
from aiohttp import web

# todo: add logging

# todo: make sure redis is running
# todo: make sure redis is configured correctly
# todo: make sure redis is not running on the same host/port as the proxy
# todo: add circuit breaker to client calls

# todo: set config params as env vars

routes = web.RouteTableDef()


def load_config(config_file):
    # todo: validate config
    with open(config_file) as f:
        return yaml.safe_load(f)


@routes.get('/{key}')
async def handle(request):
    key = request.match_info['key']
    try:
        print(f"Looking for: {key}")
        result = await proxy.get(key)
    except ConnectionError:
        return web.Response(text="Proxy server is down", status=500)
    except redis.exceptions.ConnectionError as e:
        return web.Response(text=f"Unknown error: {e}", status=500)
    if not result:
        return web.Response(text="Key not found", status=404)
    return web.Response(text=result.decode('utf-8'))


def main(proxy_ip, proxy_port, client_ip, client_port, cache_capacity, cache_expiry):
    global proxy

    proxy = redis_proxy_factory(client_ip, client_port, cache_capacity, cache_expiry)
    app = web.Application()
    app.router.add_get('/{key}', handle)

    web.run_app(app, host=proxy_ip, port=proxy_port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Redis proxy server')
    parser.add_argument('--config', type=str, help='config file', required=True)
    args = parser.parse_args()
    cfg = load_config(args.config)

    print(cfg)

    main(
        cfg['proxy']['ip'],
        cfg['proxy']['port'],
        cfg['client']['ip'],
        cfg['client']['port'],
        cfg['cache']['capacity'],
        cfg['cache']['expiry']
    )
