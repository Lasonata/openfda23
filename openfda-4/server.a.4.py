import http.server
import socketserver
import http.client
import json

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 9009

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        def send_file(file_name): # call to enter a filename to be opened
            with open(file_name) as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        def open_fda(drug, limit): # called to search for a drug and a limit

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=generic_name:%s&limit=%s" % (drug, limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            repos = json.loads(repos_raw)

            with open("fda_info_tobesent.html", "w"):
                self.wfile.write(bytes('<html><head><h1>You searched for %s drugs </h1><body style="background-color: yellow" >\n<ol>' % limit, "utf8"))

                for i in range(len(repos['results'])):
                    try:
                        drug = "<li>"+ "brand name is: " + repos['results'][i]["openfda"]["brand_name"][0] + "</li>"
                        self.wfile.write(bytes(drug, "utf8"))
                    except KeyError:
                        continue
                self.wfile.write(bytes('</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Sad"><p><a href="http://%s:%s/">Back to Main Page</a></p></head></html>' % (IP, PORT), "utf8"))

        path = self.path
        if path != "/favicon.ico":
            print("PATH: path introduced by client:", path)
        if path.find('drug') != -1:  # let´s try to find a drug and a limit entered by user
            try:
                print("SEARCHED: client has attemped to make a request")
                drugloc = path.find('drug')  # finds drug location
                limitloc = path.find('limit')  # finds limit location
                drug = path[drugloc + 5:limitloc - 1]  # drug entered by client
                limit = path[limitloc + 6:]  # limit entered by client
                print("The user asked for %s and especified a limit of %s" % (drug, limit))
                open_fda(drug, limit)
                print("client has succesfully made a request")
                filename = "fda_info_tobesent.html"
                send_file(filename)
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
                filename = "error.html"
                send_file(filename)
        elif path == "/":
            print("SEARCH: client entered search web")
            filename = "search.html"
            send_file(filename)
        else:
            if path != "/favicon.ico":
                print("***** ERROR: standard error")
            filename = "error.html"
            send_file(filename)
            # Send message back to client

        if path != "/favicon.ico":
            print("SERVED: File <<%s>> has been sent!" % filename)
            return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at %s:%s" % (IP, PORT))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")

