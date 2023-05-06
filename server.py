import socket
import email
import os

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.max_connections = 1
        self.max_recv = 4096  # 4MB
        self.root_dir = 'public/'

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(self.max_connections)

        print(f"Server started on {self.host} port {self.port} (http://{self.host}:{self.port}) ...")

        while True:
            conn, addr = self.server.accept()
            print(addr)
            with conn:
                request = conn.recv(self.max_recv).decode()
                if request:
                    response = self.handle_request(request)
                    conn.sendall(response)

    def handle_request(self, request):
        method, path, headers, body = self.parse_request(request)

        if method == "GET":
            if not path:
                path = "index.html"

            path = os.path.join(self.root_dir, path)

            if os.path.isfile(path):
                return self.make_response(self.read_file(path))
            else:
                return self.error_response(404, "File Not Found")
        elif method == "POST":
            return self.make_response(b"<h1>Not Implemented Yet.</h1>")
        else:
            return self.error_response(405, "Method Not Allowed")

    def read_file(self, filename):
        with open(filename, "rb") as f:
            return f.read()

    def parse_request(self, data):
        request, data = data.split("\r\n", 1)

        method, path, _ = request.split()
        headers = self.parse_headers(data)

        body = None
        if headers.get("Content-Length"):
            body = self.parse_body(data.split("\r\n\r\n")[-1])

        return method, path[1:], headers, body

    def parse_headers(self, data):
        headers = email.message_from_string(data)
        headers = dict(headers.items())
        return headers

    def parse_body(self, data):
        body = {}
        for pair in data.split("&"):
            key, value = pair.split("=")
            body[key] = value
        return body

    def error_response(self, code, message):
        response = f"<h1>{code} {message}</h1>".encode()
        return self.make_response(response, code, message)

    def make_response(self, body, code=200, message="OK", headers=None):
        headers = self.make_headers(code, message, headers)
        response = headers + body
        return response

    def make_headers(self, code, message, headers=None):
        response_headers = {
            'Content-Type': 'text/html',
            'Server': 'XYZ simple server',
        }
        if headers:
            response_headers.update(headers)
        headers = "\r\n".join([f"{k}: {v}" for k, v in response_headers.items()])
        headers = f"HTTP/1.1 {code} {message}\r\n{headers}\r\n\r\n"
        return headers.encode()


if __name__ == '__main__':
    server = Server('0.0.0.0', 1337)
    server.run()
