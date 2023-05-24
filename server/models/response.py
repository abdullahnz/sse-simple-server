import mimetypes

class Response:
    def __init__(self):
        self._response_buffer = b'' # Response buffer 
        self._headers_dict = []     # Headers dict
        self._headers_buffer = b''  # Headers buffer
        self._body_buffer = b''     # Body buffer
        
    def read_file(self, filename):
        """Read data from file"""
        with open(filename, "rb") as f:  # Open file in binary mode as f
            return f.read()              # Return data from file f
    
    def guess_type(self, path):
        return mimetypes.guess_type(path)[0] or ''   # Guess file type from path and return it or return empty string
   
    def send_header(self, keyword: str, value: str):
        """Add header to headers buffer"""
        self._headers_dict.append(f'{keyword}: {value}'.encode())   # Append header to headers buffer as bytes string (b'Content-Type: text/html')
    
    def flush_headers(self):
        self._headers_buffer = b'\r\n'.join(self._headers_dict) + b'\r\n\r\n'   # Join headers buffer with \r\n and add \r\n\r\n to the end
        self._headers_dict = []                                                 # Clear headers buffer

    def send_response_header(self, code, message):
        self._response_buffer = f'HTTP/1.1 {code} {message}\r\n'.encode()       # Set response buffer to HTTP/1.1 {code} {message}\r\n as bytes string (b'HTTP/1.1 200 OK\r\n')
        
    def send_body(self, body):
        if isinstance(body, str):                   # If body is string
            body = body.encode()                    # Encode body to bytes string
        self._body_buffer = body + b'\r\n'          # Set body buffer to body + \r\n as bytes string (b'Hello, World!\r\n')
    
    def send_response(self, body, code = 200, message = 'OK'):
        self.send_header('Server', 'SSE Server')                # Add Server header to headers buffer (b'Server: SSE Server')
        self.send_response_header(code=code, message=message)   # Add response header to response buffer (b'HTTP/1.1 200 OK\r\n')
        self.flush_headers()                                    # Flush headers buffer
        self.send_body(body)                                    # Add body to body buffer (b'Hello, World!\r\n')
        return self._response_buffer + self._headers_buffer + self._body_buffer      # Return all response buffer 
        
    def error_response(self, code, message):
        body = f'<h1>{code} {message}</h1>'.encode()    # Set body to <h1>{code} {message}</h1> as bytes string
        self.send_header('Content-Type', 'text/html')   # Add Content-Type header to headers buffer
        return self.send_response(body, code=code, message=message) # Return response buffer with body, code and message
    
    def render_file(self, path):
        self.send_header('Content-Type', self.guess_type(path)) # Add Content-Type header to headers buffer
        return self.send_response(self.read_file(path))         # Return response buffer with data from file
        
    def redirect(self, path):
        self.send_header('Location', path)                                      # Add Location header to headers buffer
        return self.send_response(b'Redirecting...', code=302, message='Found') # Return response buffer with body, code and message
    