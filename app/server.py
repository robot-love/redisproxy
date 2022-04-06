from core.proxy import redis_proxy_factory

import socketserver

import logging
import sys
import socket
import threading
import signal


class ClientThread(threading.Thread):
    """
    ClientThread class

    Impl copied from: http://net-informations.com/python/net/thread.htm
    """
    def __init__(self, client_addr, client_socket):
        threading.Thread.__init__(self)
        self.csocket = client_socket
        logging.info(f"New connection added: {client_addr[0]}:{client_addr[1]}")
        self._client_host = client_addr[0]
        self._client_port = client_addr[1]

    def run(self):
        logging.info(f"Connection from: {self._client_host}")
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()

            if not msg:
              break

            logging.info(f"from client: \n{msg}")
            self.csocket.send(bytes("Received.", 'UTF-8'))

        logging.info(f"Client at {self._client_host} disconnected...")


class MultiThreadedServer:
    def __init__(self, host, port, proxy):
        self.host = host
        self.port = port
        self.proxy = proxy
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        logging.info("Server started")

    def listen(self):
        logging.info("Listening for connections")
        while True:
            self.sock.listen(1)
            client, address = self.sock.accept()
            ct = ClientThread(address, client)
            ct.start()

    def stop(self):
        self.sock.close()
        logging.info("Server stopped")


def alt_main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    server = MultiThreadedServer('localhost', 8888, redis_proxy_factory('localhost', 6379, 10, 10))
    server.listen()

if __name__ == '__main__':
    srv = socketserver.TCPServer()