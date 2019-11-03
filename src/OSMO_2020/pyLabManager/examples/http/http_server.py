from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

# https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
# This class will handles any incoming request from
# the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("Hello World !")
        return
        # Handler for the CUSTOM requests
    def do_CUSTOM(self):
        # Send a proper HTTP response
        self.send_response(200)
        # https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
        self.send_header('Content-type', 'text')
        self.end_headers()
        # Send the message
        self.wfile.write("Custom Message!")
        return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('localhost', 8080), myHandler)
	print 'Started httpserver on port ' , 8080
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
