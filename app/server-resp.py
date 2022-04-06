from core.proxy import redis_proxy_factory

import logging
from asyncio import run
from asyncio.streams import start_server, StreamReader, StreamWriter


def parse_resp_get(resp):
    resp = resp.decode('utf-8')
    assert resp[:8] == "*2$3GET$"
    for i,c in enumerate(resp[8:]):
        if not c.isdigit():
            return resp[8+i:]


async def handle(reader: StreamReader, writer: StreamWriter):
    data = await reader.read(2048)
    logging.info(f'New connection: {data}')

    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message!r} from {addr!r}")
    reply = parse_resp_get(data).encode('utf-8')
    print(f"Send: {reply!r}")

    writer.write(reply)
    await writer.drain()


async def main():
    srv = await start_server(handle, 'localhost', 8888)
    addrs = ', '.join(str(sock.getsockname()) for sock in srv.sockets)
    print(f'Serving on {addrs}')

    async with srv:
        await srv.serve_forever()

run(main())
