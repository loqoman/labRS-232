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
    def do_ASSINGLABKEY(self):
        # Send a proper HTTP response
        self.send_response(200)
        # https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
        self.send_header('Content-type', 'text')
        self.end_headers()
        # Send the message
        self.wfile.write("Custom Message!")
        return

    def do_PUT(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print(post_data)

    def do_ASSIGN(self):
        # Psudocode
        # RESTFUL, all happens after a request from client
        '''
        -1. If there is unsent, linked data send it back 
        -1a.(GOTO 1)

        0. Check table for unassigned data
        0a. Send data back with the sample ID if there is unassigned data

        1. Parse the sample ID
        2. Set a flag linking the sample ID to the next data set
        <Once data is avaible>
        3. Store the data w/ ID in 'database'
        '''



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
