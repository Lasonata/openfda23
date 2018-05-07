import http.server
import socketserver
import http.client
import json

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000
socketserver.TCPServer.allow_reuse_adress = True

# HTTPRequestHandler class
class OpenFDAClient():
# include the logic to communicate with the OpenFDA remote API

    def send_query(self, request_ending): # useful to obtain a jsonlist
        # send a query (implemented by request_ending) and returns the data obtained from the search
        request_default = "/drug/label.json"
        full_query = request_default + '?' + request_ending

        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", full_query, None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()

        repos = json.loads(repos_raw)
        return repos

    def list_drugs(self, limit = 10): # useful for drug_list, warning_list, company_list (just limit paremeter os requiered)
        # implements request by adding a limit parameter and call send_request to obtain the corresponding Json list
        request_ending = "limit=%s" % (limit)
        json_list = self.send_query(request_ending)
        print('json list has been returned: parameters: limit = %s' % limit)
        return json_list

    def search_drugs(self, active, limit = 10): # useful for active_ingredient
        # implements request by adding an active_ingredient and a limit parameter to obtain the corresponding Json list
        request_ending = "search=active_ingredient:%s&limit=%s" % (active, limit)
        json_list = self.send_query(request_ending)
        print('json list has been returned: parameters: active = %s , limit = %s' % (active, limit))
        return json_list

    def search_companies(self, manufacturer, limit = 10):  # searches for manufacturer_name / returns brand_name
        # implements request by adding a manufacturer_name and limit parameter to obtain the corresponding Json list
        request_ending = "search=openfda.manufacturer_name:%s&limit=%s" % (manufacturer, limit)
        json_list = self.send_query(request_ending)
        print('json list has been returned: parameters: manufacturer = %s , limit = %s' % (manufacturer, limit))
        return json_list


class OpenFDAParser():
# includes the logic to extract the data from drugs items
    def parse_drugs(self, json_list): # useful in active_ingredients, manufacturer_list
        # called to return a list containing brand_names:
        brand_list = []
        for i in range(len(json_list['results'])):
            try:
                for n in range(len(json_list['results'][i]["openfda"]["brand_name"])):
                    try:
                        brand_list.append(json_list['results'][i]["openfda"]["brand_name"][0])
                    except KeyError:
                        brand_list.append("Unknown")
                        break
            except KeyError:
                brand_list.append("Unknown")
                continue
        return brand_list

    def parse_warnings(self, json_list): # useful for warning_list
    # called to return a list containing warnings
        warning_list = []
        for i in range(len(json_list['results'])):
            try:
                for n in range(len(json_list['results'][i]["openfda"]["brand_name"])):
                    try:
                        warning_list.append(json_list['results'][i]["warnings"][0])
                    except KeyError:
                        warning_list.append("Unknown")
                        break
            except KeyError:
                warning_list.append("Unknown")
                continue
        return warning_list

    def parse_companies(self, json_list): # useful for manufacturer_list
        # called to return a list containing manufacturers
        manufacturer_list = []
        for i in range(len(json_list['results'])):
            try:
                for n in range(len(json_list['results'][i]["openfda"]["manufacturer_name"])):
                    try:
                        manufacturer_list.append(json_list['results'][i]["openfda"]["manufacturer_name"][0])
                    except KeyError:
                        manufacturer_list.append("Unknown")
                        break
            except KeyError:
                manufacturer_list.append("Unknown")
                continue
        return manufacturer_list

class OpenFDAHTML():

    def create_html(self, json_list): # useful for all
        # takes in a jasonlist and writes element by element in an html file
        html_file = "<ul>"
        for elem in json_list:
            html_file += "<li>" + elem + "</li>"
        html_file += "</ul>"
        html_file += "<marquee>powered by Lasonata</marquee>"
        print("html file has been built")
        return html_file

    def send_file(self, file):
        with open(file, "r") as f:
            content = f.read()
        print(file, "is to be sent")
        return content

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        # let's create three instances
        client = OpenFDAClient()
        parser = OpenFDAParser
        html = OpenFDAHTML

        code = False # unless told otherwise # will send error.html
        path = self.path
        if path != "/favicon.ico":
            print("_____path is: %s_____" % path)

        if path == "/":
        # default
            print("SEARCH: client entered default search web")
            code = "start"

        elif path.find('searchDrug') != -1:
        # input = active_ingredient // output = drugs with such active_ingredient
            try:
                print("SEARCHED: client has attemped to make a request")
                active = path.split("=")[1].split("&")[0]
                try:
                    limit = path.split("=")[2]
                except IndexError:
                    limit = 10
                print("REQUEST: Client asked for drugs with %s and specified a limit of %s" % (active, limit))
                json_list = client.search_drugs(active, limit) # getting Json data
                content = parser.parse_drugs(self, json_list) # getting a list of drugs
                code = True
                print("SUCCESS: Client has successfully made a request")
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
        elif path.find('searchCompany') != -1:
        # input = manufacturer and a limit // output = drugs produced by such company
            try:
                print("SEARCHED: client has attemped to make a request")
                manufacter = path.split("=")[1].split("&")[0]
                try:
                    limit = path.split("=")[2]
                except IndexError:
                    limit = 10
                print("REQUEST: Client asked for drugs produced by %s and especified a limit of %s" % (manufacter, limit))
                json_list = client.search_companies(manufacter, limit)
                content = parser.parse_drugs(self, json_list)
                code = True
                print("SUCCESS: Client has successfully made a request")
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
        elif path.find('listDrugs') != -1:
        # input = limit // output = list of drugs
            try:
                print("SEARCHED: client has attemped to make a request")
                try:
                    limit = path.split("=")[1]
                except IndexError:
                    limit = 10
                print("Client asked for a drug list and specified a limit of %s" % (limit))
                json_list = client.list_drugs(limit)
                content = parser.parse_drugs(self, json_list)
                code = True
                print("SUCCESS: Client has successfully made a request")
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
        elif path.find('listCompanies') != -1:
        # input = limit // output = list of companies
            try:
                print("SEARCHED: client has attemped to make a request")
                try:
                    limit = path.split("=")[1]
                except IndexError:
                    limit = 10
                print("Client asked for a manufacturer list and especified a limit of %s" % (limit))
                json_list = client.list_drugs(limit)
                content = parser.parse_companies(self, json_list)
                code = True
                print("SUCCESS: Client has successfully made a request")
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
        elif path.find('listWarnings') != -1:  # let´s try to find a manufacturer and a limit entered by user
            try:
                print("SEARCHED: client has attemped to make a request")
                try:
                    limit = path.split("=")[1]
                except IndexError:
                    limit = 10
                print("Client asked for a warning list and especified a limit of %s" % (limit))
                json_list = client.list_drugs(limit)
                content = parser.parse_companies(self, json_list)
                code = True
                print("SUCCESS: Client has successfully made a request")
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
        else:
            if path != "/favicon.ico":
                print("* * ERROR * * : standard error: wrong path")
                code = False

        # let´s send the appropriate header
        if code:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if code == "start":
                send_content = html.send_file(self, "search.html")
            else:
                send_content = html.create_html(self, content) # writing down list in an html file
        elif "secret" in path:
            self.send_response(401)
            self.send_header("WWW-Authenticate", "Basic realm='OpenFDA Private Zone")
            self.end_headers()

        elif "redirect" in path:
            self.send_response(302)
            self.send_header('Location', 'http://localhost:8000/')
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            send_content = html.send_file(self, "error.html")

        # Send message back to client
        if path != "/favicon.ico":
            self.wfile.write(bytes(send_content, "utf8"))
            print("SERVED: File has been sent!")


# Handler = http.server.SimpleHTTPRequestH andler # author: Lasonata
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

