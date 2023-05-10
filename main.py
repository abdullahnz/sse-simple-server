from server import Server

class Auth(Server):
    def do_GET(self, req, res):
        auth = req.cookies.get('auth')
        if not auth:
            return res.render_file('public/login.html')
        
        return res.send_response(f"<h1>Hello, {auth}</h1>".encode())

    def do_POST(self, req, res):
        username = req.body.get('username')
        password = req.body.get('password')
        
        if username == "guest" and password == "guest":
            res.send_header('Set-Cookie', f'auth={username}')
        
        return res.redirect(req.path)

if __name__ == '__main__':
    server = Server(host='0.0.0.0', port=8080, root_dir="public")
    server.add_route(path="/auth", handler=Auth)
    server.run()

