from app.proxy import RedisProxy

from http.server import HTTPServer, BaseHTTPRequestHandler


class RedisProxyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.path
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(self.path, 'utf-8'))


if __name__ == '__main__':
    global proxy = RedisProxy('localhost', 5000, 20, 10)
    srv = HTTPServer(('localhost', 9999), RedisProxyRequestHandler)
    srv.serve_forever()