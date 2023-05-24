import email

class Request:
    def __init__(self, buffer):    
        request, data = buffer.split("\r\n", 1)     # Split request and data from buffer (request is the first line, data is the rest)

        method, path, _ = request.split()           # Split request to method, path, and protocol (GET / HTTP/1.1)
        
        self.method = method                        # Method (GET, POST, etc.)
        self.path = path                            # Path (/, /auth, etc.)
        self.headers = self.parse_headers(data)     # Headers dict (Content-Type, Content-Length, etc.)
        self.cookies = self.parse_cookies(self.headers.get('Cookie'))   # Cookies dict (auth, etc.)
        self.body = self.parse_body(data.split("\r\n\r\n")[-1])         # Body dict (username, password, etc.)

    def parse_headers(self, data):  
        headers = email.message_from_string(data)       # Parse headers from data using email module
        headers = dict(headers.items())                 # Convert headers to dict
        return headers

    def parse_body(self, body):
        return dict([x.split('=') for x in body.split('&')] if body else '')            # Convert body to dict
    
    def parse_cookies(self, cookies):
        return dict([x.split('=', 1) for x in cookies.split('; ')] if cookies else '')  # Convert cookies to dict
