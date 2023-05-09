import socket, os, re
from .models.request import Request

SERVER_NAME = 'XYZ Server'

class Server:
    def __init__(self, host, port, root_dir = './'):
        self.host = host
        self.port = port
        self.server = None
        self.max_connections = 1
        self.max_recv = 4096  # 4MB
        self.root_dir = root_dir
        self.routes = {}

    def run(self):
        """Running socket server"""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(self.max_connections)

        print(f"Server started on {self.host} port {self.port} (http://{self.host}:{self.port}) ...")

        while True:
            client_sock, client_addr = self.server.accept()
            with client_sock:
                try:
                    client_request = client_sock.recv(self.max_recv).decode()
                    if client_request:
                        response = self.handle_request(client_addr, client_request)
                except Exception as e:
                    response = self.error_response(500, "Internal Server Error")
                
                client_sock.sendall(response)
    
    def add_route(self, path, handler):
        """Add custom route and handler"""
        self.routes[path] = handler

    def handle_request(self, addr, request):
        """Handling request data from client"""
        request = Request(request)
        
        print(f"{addr}: {request.method=}, {request.path=}")
        
        chrome_regex = r'^(?!.*Edge).*Chrome'
        if not re.match(chrome_regex, request.headers.get('User-Agent')):
            return self.error_response(403, "Forbidden")
        
        callback = self.routes.get(request.path)
        if callback:
            handler_method = 'do_' + request.method
            if hasattr(callback, handler_method):
                return getattr(callback, handler_method)(self, request)
            return self.error_response(405, "Method not Allowed")
        
        if request.path == '/':
            request.path = '/index.html'
        
        request.path = self.root_dir + request.path
        if os.path.isfile(request.path):
            return self.make_response(self.read_file(request.path))
        return self.error_response(404, "File Not Found")
        
    def read_file(self, filename):
        """Read data from file"""
        with open(filename, "rb") as f:
            return f.read()
        
    def make_headers(self, code, message, headers=None):
        """Add custom header and return the response headers"""
        response_headers = {
            'Content-Type': 'text/html',
            'Server': SERVER_NAME,
        }
        if headers:
            response_headers.update(headers)
        headers = "\r\n".join([f"{k}: {v}" for k, v in response_headers.items()])
        headers = f"HTTP/1.1 {code} {message}\r\n{headers}\r\n\r\n"
        return headers.encode()

    def make_response(self, body, code=200, message="OK", headers=None):
        """Craft response header and body"""
        headers = self.make_headers(code, message, headers)
        response = headers + body
        return response
    
    def error_response(self, code, message):
        """Make error response as h1 html template"""
        response = f"<h1>{code} {message}</h1>".encode()
        return self.make_response(response, code, message)
    
    def redirect(self, path, headers = None):
        """Make a redirect to path argument"""
        headers.update({'Location': path})
        return self.make_headers(302, "Found", headers=headers)
    
    def render_file(self, path):
        return self.make_response(self.read_file(path))