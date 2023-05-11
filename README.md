# SSE Web Server

Simple Safe Exam (SSE) Web Server is a simple web server implementation of **TCP Socket** written in python required for final presentation of **network computer practicum** courses. This server only accepts clients to access with a specific browser applications. As additional info, for now SSE Web Server only authorizes browsers that use the **Chromium** browser engine to be able to access it.
## Basic Template Usage

Here is simple basic template for implementing this socket server, or you can see main.py for the example.

```py
from server import Server

class HelloWorld(Server):
    def do_GET(self, req, res):
        return res.send_response('Hello, World!')

    def do_POST(self, req, res):
        return res.render_file('...')

if __name__ == '__main__':
    server = Server(host='0.0.0.0', port=8080, root_dir='public')
    server.add_route(path='/', handler=HelloWorld)
    server.run()
```

## Our Members

- Gloria Natasya Irene Sidebang - 1301213445
- Bintang FJM Sujono - 1301213531
- Nizam Abdullah - 1301213232

