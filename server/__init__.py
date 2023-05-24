from .models.request import Request
from .models.response import Response
import threading, socket, os, re

class Server:
    def __init__(self, host, port, root_dir = './'):
        self.host = host            # Hostname or IP address
        self.port = port            # Port number
        self.server = None          # Server socket object
        self.max_connections = 1    # Max connections 
        self.max_recv = 4096        # Max receive data size 
        self.root_dir = root_dir    # Root directory for static files
        self.routes = {}            # Routes dict for custom routes and handlers

    def run(self):
        """Running socket server"""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object (TCP)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)       # Prevent socket.error: [Errno 48] Address already in use
        self.server.bind((self.host, self.port))                                # Bind to the server host and port
        self.server.listen(self.max_connections)                                # Now wait for client connection.
        
        # Display server info to console
        print(f"Server started on {self.host} port {self.port} (http://{self.host}:{self.port}) ...")

        # Server's main loop (infinite loop)
        while True:
            client_sock, client_addr = self.server.accept()     # Establish connection with client. (accept client connection)
            threading.Thread(   
                target=self.handle_connection,                  # Start a new thread for handle client's request by calling
                args=(client_sock, client_addr)                 # handle_connection method with client_sock and client_addr as arguments
            ).start()                                           
    
    def handle_connection(self, client_sock, client_addr):
        """Client connection's handler"""
        with client_sock:                                                   # Close socket when done (`with` statement)
            client_request = client_sock.recv(self.max_recv).decode()       # Receive request from client 
            if client_request:                                              # If client request is not empty (client request is exist)
                client_sock.sendall(
                    self.handle_request(client_addr, client_request)        # Send all response to client by calling handle_request method client's attribute as arguments
                )
                
    def add_route(self, path, handler):
        """Add custom route and handler"""
        self.routes[path] = handler         # Add route and handler to routes dict (path as key, handler as value)

    def handle_request(self, addr, request, response = Response()):
        """Handling request data from client"""
        request = Request(request)                                      # Parse raw request data to Request object
        
        print(f"{addr}: {request.method=}, {request.path=}")            # Display request info to console
        
        
        try:                                                            # Handling request
            chrome_reg = r'^(?!.*Edge).*Chrome'                         # Regex for chrome browser user agent
            client_browser = request.headers.get('User-Agent') or ''    # Get client browser user agent
            
            if not re.match(chrome_reg, client_browser):                # If client browser is not chrome
                return response.error_response(403, "Forbidden")        # Return 403 Forbidden (only chrome browser allowed)
            
            callback = self.routes.get(request.path)                    # Get callback from routes dict
            
            if callback:                                                    # If callback is not None (there is a handler for this path)
                handler_method = 'do_' + request.method                     # Get handler method name
                if hasattr(callback, handler_method):                       # If handler method is exist in callback
                    return getattr(callback, handler_method)(self, request, response)       # Call handler method with self, request, and response as arguments
                return response.error_response(405, "Method not Allowed")   # Return 405 Method not Allowed
            
            if request.path == '/':                 # If request path is root path
                request.path = '/index.html'        # Set request path to index.html (default page)
            
            request.path = self.root_dir + request.path     # Set request path to root_dir + request path
            
            if os.path.isfile(request.path):                # If request path is file and exist in root_dir
                return response.render_file(request.path)   # Return file content as response
            
            return response.error_response(404, "File Not Found")   # Return 404 File Not Found
            
        except Exception as e:                                              # If error occured while handling request
            return response.error_response(500, "Internal Server Error")    # Return 500 Internal Server Error 
        