from core.proxy import aio_redis_proxy_factory
from core.parser import parse_resp_get_for_key, encode_resp_get_response

import logging
from asyncio import run
from asyncio.streams import start_server, StreamReader, StreamWriter
from os import environ


logging.basicConfig(level=logging.DEBUG)


async def handle(reader: StreamReader, writer: StreamWriter):
    data = await reader.read(2048)
    logging.info(f'New connection: {data}')
    global proxy
    message = data.decode()
    addr = writer.get_extra_info('peername')
    logging.debug(f"Received {message!r} from {addr!r}")
    try:
        key = parse_resp_get_for_key(data)
        logging.debug(f"Requested key: {key}")
        value = await proxy.get(key)
        if not value:
            value = ""
            logging.debug(f"Value: {value}")
        else:
            logging.debug(f"No value found for key: {key}")
        reply = encode_resp_get_response(value)
        writer.write(reply)
    except AssertionError:
        logging.debug("Not a GET request")
        writer.write(b'-ERR: malformed GET request.\r\n')
    finally:
        await writer.drain()
        writer.close()


async def main():
    global proxy
    proxy = aio_redis_proxy_factory(environ['CLIENT_HOST'], environ['CLIENT_PORT'], int(environ['CACHE_CAPACITY']), int(environ['CACHE_EXPIRY']))
    srv = await start_server(handle, environ['PROXY_HOST'], environ['PROXY_PORT'])
    addrs = ', '.join(str(sock.getsockname()) for sock in srv.sockets)
    logging.info(f'Serving on {addrs}')

    async with srv:
        await srv.serve_forever()

run(main())
