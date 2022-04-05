from core.proxy import redis_proxy_factory, aio_redis_proxy_factory

import redis.exceptions
from aiohttp import web
from os import environ

# todo: add logging
# todo: add circuit breaker to client calls

routes = web.RouteTableDef()


@routes.get('/{key}')
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
    return web.Response(text=result.decode('utf-8'))


def main(proxy_host, proxy_port, client_host, client_port, cache_capacity, cache_expiry):
    global proxy

    proxy = aio_redis_proxy_factory(client_host, client_port, cache_capacity, cache_expiry)
    app = web.Application()
    app.router.add_get('/{key}', handle)

    web.run_app(app, host=proxy_host, port=proxy_port)


if __name__ == '__main__':
    main(
        environ['PROXY_HOST'], 
        int(environ['PROXY_PORT']),
        environ['CLIENT_HOST'],
        int(environ['CLIENT_PORT']),
        int(environ['CACHE_CAPACITY']),
        int(environ['CACHE_EXPIRY'])
    )
