import http.server
import socketserver
import http.client
import json

# -- IP and the port of the server
IP = "10.3.52.149"  # Localhost means "I": your local machine
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

        def send_file(file_name):
            with open(file_name) as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))
        def send_10drugs():
            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "https://api.fda.gov/drug/label.json?limit=10", None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            repos = json.loads(repos_raw)
            conn.close()

            with open("html_file_2.html", "w"):
                self.wfile.write(bytes('<html><head><h1>Here you are:</h1><body style="background-color: yellow">\n<ol>', "utf8"))
                for i in range(len(repos['results'])):
                    try:
                        drug = '<li>' + repos['results'][i]["openfda"]["generic_name"][0] + '</li>'
                        self.wfile.write(bytes(drug, "utf8"))
                    except KeyError:
                        continue
                self.wfile.write(bytes('</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Sad"><p><a href="http://%s:%s/">Back to Main Page</a></p></head></html>' % (IP, PORT), "utf8"))

        path = self.path
            # Send message back to client
        if path == "/":
            send_file("html_file.html")
        elif "10drugs" in path:
            send_10drugs()
        else:
            print("path error")
            send_file('error.html')
        print("File served!")
        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")




# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open("htmlopenfda3.html", "r") as f:
             message= f.read()
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")

