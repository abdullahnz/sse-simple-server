from server import Server  # Import Server class from server package as a base server class.

class Auth(Server):
    def do_GET(self, req, res):
        """GET method handler"""
        auth = req.cookies.get('auth')                  # Get auth cookie from request cookies
        if not auth:                                    # If auth cookie is not set 
            return res.render_file('public/login.html') # Render login page
        
        return res.send_response(f"<h1>Hello, {auth}</h1>".encode()) # Else render hello page with username from auth cookie

    def do_POST(self, req, res):
        """POST method handler"""
        username = req.body.get('username')         # Get username from request body 
        password = req.body.get('password')         # Get password from request body
        
        if username == "guest" and password == "guest":         # If username and password are correct
            res.send_header('Set-Cookie', f'auth={username}')   # Set auth cookie
        
        return res.redirect(req.path)               # Redirect to /auth path

if __name__ == '__main__':
    server = Server(host='0.0.0.0', port=8080, root_dir="public")   # Create server instance with root_dir
    server.add_route(path="/auth", handler=Auth)                    # Add route to server instance with Auth class as handler for /auth path
    server.run()                                                    # Run server

