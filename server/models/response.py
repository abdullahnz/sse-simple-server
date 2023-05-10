import mimetypes

class Response:
    def __init__(self):
        self._response_buffer = b''
        self._headers_dict = []
        self._headers_buffer = b''
        self._body_buffer = b''
    
    def read_file(self, filename):
        """Read data from file"""
        with open(filename, "rb") as f:
            return f.read()
    
    def guess_type(self, path):
        return mimetypes.guess_type(path)[0] or ''
   
    def send_header(self, keyword: str, value: str):
        """Add header to headers buffer"""
        if not hasattr(self, '_headers_dict'):
            self._headers_dict = []
        self._headers_dict.append(f'{keyword}: {value}'.encode())
    
    def flush_headers(self):
        if not hasattr(self, '_headers_buffer'):
            self._headers_dict = []
        self._headers_buffer = b'\r\n'.join(self._headers_dict) + b'\r\n\r\n'
        self._headers_dict = []

    def send_response_header(self, code, message):
        self._response_buffer = f'HTTP/1.1 {code} {message}\r\n'.encode()
        
    def send_body(self, body):
        if isinstance(body, str):
            body = body.encode()
        self._body_buffer = body + b'\r\n'
    
    def send_response(self, body, code = 200, message = 'OK'):
        self.send_header('Server', 'SSE Server')
        self.send_response_header(code=code, message=message)
        self.flush_headers()
        self.send_body(body)
        return self._response_buffer + self._headers_buffer + self._body_buffer
        
    def error_response(self, code, message):
        body = f'<h1>{code} {message}</h1>'.encode()
        self.send_header('Content-Type', 'text/html')
        return self.send_response(body, code=code, message=message)
    
    def render_file(self, path):
        self.send_header('Content-Type', self.guess_type(path))
        return self.send_response(self.read_file(path))
        
    def redirect(self, path):
        self.send_header('Location', path)
        return self.send_response(b'Redirecting...', code=302, message='Found')
    