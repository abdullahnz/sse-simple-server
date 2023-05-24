import email

class Request:
    def __init__(self, buffer):    
        request, data = buffer.split("\r\n", 1)

        method, path, _ = request.split()
        
        self.method = method    # GET or POST
        self.path = path        
        self.headers = self.parse_headers(data)     # Headers dict
        self.cookies = self.parse_cookies(self.headers.get('Cookie'))   # Cookies dict
        self.body = self.parse_body(data.split("\r\n\r\n")[-1])         # Body dict

    def parse_headers(self, data):  
        headers = email.message_from_string(data)       # Parse headers from data
        headers = dict(headers.items())                 # Convert headers to dict
        return headers

    def parse_body(self, body):
        return dict([x.split('=') for x in body.split('&')] if body else '')    # Convert body to dict
    
    def parse_cookies(self, cookies):
        return dict([x.split('=', 1) for x in cookies.split('; ')] if cookies else '')  # Convert cookies to dict
