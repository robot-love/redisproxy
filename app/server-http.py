from core.proxy import redis_proxy_factory, aio_redis_proxy_factory

import redis.exceptions
from aiohttp import web
from os import environ
import asyncio
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logging.getLogger().addHandler(logging.FileHandler('aioredis_access.log'))

routes = web.RouteTableDef()
sem = asyncio.Semaphore(int(environ['CONCURRENT_MAX']))


async def handle(request):
    key = request.match_info['key']
    try:
        result = await proxy.get(key)
    except redis.exceptions.ConnectionError as e:
        return web.Response(text=f"Database is not available : {e}", status=500)
    except Exception as e:
        return web.Response(text=f"Unknown error : {e}", status=500)
    if not result:
        return web.Response(text="Key not found", status=404)
    return web.Response(text=result)


@routes.get('/{key}')
async def safe_handle(request):
    """
    Request handler function with max-concurrency limit.

    Seems almost hilarious to use a task counter (a global variable no less) to rate-limit the number of concurrent
    requests, instead of a semaphore.
    """
    if sem.locked():
        logging.debug(f"Too many concurrent tasks, rejecting request for {request.match_info['key']}")
        return web.Response(text="Too many requests", status=429)
    async with sem:
        logging.debug(f"Starting task for {request.match_info['key']}.")
        value = await handle(request)
    logging.debug(f"Task for {request.match_info['key']} completed.")
    return value


def main(proxy_host, proxy_port, client_host, client_port, cache_capacity, cache_expiry):
    global proxy

    proxy = aio_redis_proxy_factory(client_host, client_port, cache_capacity, cache_expiry)
    app = web.Application()
    app.router.add_get('/{key}', safe_handle)

    web.run_app(app, host=proxy_host, port=proxy_port)


if __name__ == '__main__':
    main(
        environ['PROXY_HOST'], 
        int(environ['PROXY_PORT']),
        environ['CLIENT_HOST'],
        int(environ['CLIENT_PORT']),
        int(environ['CACHE_CAPACITY']),
        int(environ['CACHE_EXPIRY']),
    )
