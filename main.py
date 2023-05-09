from server import Server

class Auth(Server):
    def do_GET(self, request):
        auth = request.cookies.get('Auth')
        if not auth:
            return self.render_file('public/login.html')
        
        return self.make_response(f"<h1>Hello, {auth}</h1>".encode())

    def do_POST(self, request):
        username = request.body.get('username')
        password = request.body.get('password')

        auth = {}
        if username == "guest" and password == "guest":
            auth.update({"Set-Cookie": f"Auth={username}"})

        return self.redirect(request.path, headers=auth)

if __name__ == '__main__':
    server = Server(host='0.0.0.0', port=8080, root_dir="public")
    server.add_route(path="/auth", handler=Auth)
    server.run()

