import socket
import email

SERVER_ADDR = (HOST, PORT) = '0.0.0.0', 4444
REQUEST_MAX_QUEUE = 1
MAX_RECV = 4096 # 4MB

HTTP_VERSION = "1.1"

HEADERS = b'''Content-Type: text/html
Server: XYZ simple server
\r\n''' 

def http_header(status_code, phrase):
    header  = f"HTTP/{HTTP_VERSION} {status_code} {phrase}\r\n".encode()
    header += HEADERS
    return header


def parse_requests(raw_data):
    request, headers = raw_data.split('\r\n', 1)
    
    headers = email.message_from_string(headers)
    headers = dict(headers.items())
    
    return request, headers


def handle_requests(sock, addr):
    """
    Handling requests from client.
    NOTE: addr argument not implemented yet.
    """
    try:
        # received raw data from client 
        client_requests = sock.recv(MAX_RECV).decode()
        
        print(client_requests)
        
        # parse raw data from client
        request, headers = parse_requests(client_requests)
        
        # print(request)
        # print(headers)
        
        method, path, version = request.split()
        
        # TODO: add other method handler 
        # ...
        if method == 'GET':
            if path == '/':
                path = '/index.html'
            
            try:
                sock.send(http_header(200, "OK"))
            except OSError:
                path = '/404.html'
                sock.send(http_header(404, "Not Found"))
                
            body = open(path[1:], 'rb').read()
            
            for line in body.splitlines():
                sock.send(line + b'\n')
            sock.send(b'\r\n')
            
    except Exception as e:
        print(f"Error occured: {e}")

if __name__ == '__main__':
    # inisiasi socket server berbasis TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # inisiasi option bla2
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind server ke host port yang ditentukan
    server.bind((HOST, PORT))
    
    # wait for connection
    server.listen(REQUEST_MAX_QUEUE)
    
    # print info
    print(f"Server started on {HOST} port {PORT} (http://{HOST}:{PORT}) ...")

    while True:
        # terima koneksi dari client (yang sudah jabat tangan | handshaking)
        client_sock, client_addr = server.accept()
        
        # handle requets
        handle_requests(client_sock, client_addr)
        client_sock.close()

    server.close() # unreachable




