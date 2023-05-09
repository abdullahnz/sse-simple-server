import email

class Request:
    def __init__(self, buffer):    
        request, data = buffer.split("\r\n", 1)

        method, path, _ = request.split()
        
        self.method = method
        self.path = path
        self.headers = self.parse_headers(data)
        self.cookies = self.parse_cookies(self.headers.get('Cookie'))
        self.body = self.parse_body(data.split("\r\n\r\n")[-1])

    def parse_headers(self, data):
        headers = email.message_from_string(data)
        headers = dict(headers.items())
        return headers

    def parse_body(self, body):
        return dict([x.split('=') for x in body.split('&')] if body else '')
    
    def parse_cookies(self, cookies):
        return dict([x.split('=', 1) for x in cookies.split('; ')] if cookies else '')
