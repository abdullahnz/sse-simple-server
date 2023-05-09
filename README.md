# SSE Web Server

Simple Safe Exam (SSE) Web Server is a simple web server implementation of **TCP Socket** written in python required for final presentation of **network computer practicum** courses. This server only accepts clients to access with a specific browser applications. In additional info, for now SSE Web Server just authorize **Chrome** browser to access.

## Basic Template Usage

Here is simple basic template for implementing this socket server, or you can see main.py for the example.

```py
from server import Server

class Home(Server):
    def do_GET(self, request):
        return self.make_response(b'Hello, World')

    def do_POST(self, request):
        return self.redirect('/some_path')

if __name__ == '__main__':
    server = Server(host='0.0.0.0', port=8080, root_dir="public")
    server.add_route(path="/", handler=Home)
    server.run()
```

## Our Members

- Gloria Natasya Irene Sidebang - 1301213445
- Bintang FJM Sujono - 1301213531
- Nizam Abdullah - 1301213232

