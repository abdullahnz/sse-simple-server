from .models.request import Request
from .models.response import Response
import threading, socket, os, re

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
            threading.Thread(
                target=self.handle_connection, 
                args=(client_sock, client_addr)
            ).start()
    
    def handle_connection(self, client_sock, client_addr):
        """Client connection's handler"""
        with client_sock:
            client_request = client_sock.recv(self.max_recv).decode()
            if client_request:
                client_sock.sendall(
                    self.handle_request(client_addr, client_request)
                )
                
    def add_route(self, path, handler):
        """Add custom route and handler"""
        self.routes[path] = handler

    def handle_request(self, addr, request, response = Response()):
        """Handling request data from client"""
        request = Request(request)
        
        print(f"{addr}: {request.method=}, {request.path=}")
        
        try:
            chrome_reg = r'^(?!.*Edge).*Chrome'
            client_browser = request.headers.get('User-Agent') or ''
            
            if not re.match(chrome_reg, client_browser):
                return response.error_response(403, "Forbidden")
            
            callback = self.routes.get(request.path)
            
            if callback:
                handler_method = 'do_' + request.method
                if hasattr(callback, handler_method):
                    return getattr(callback, handler_method)(self, request, response)
                return response.error_response(405, "Method not Allowed")
            
            if request.path == '/':
                request.path = '/index.html'
            
            request.path = self.root_dir + request.path
            
            if os.path.isfile(request.path):
                return response.render_file(request.path)
            
            return response.error_response(404, "File Not Found")
            
        except Exception as e:
            return response.error_response(500, "Internal Server Error")
        