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
    def send_file(self, file_name): # call to enter a filename to be opened
        with open(file_name) as f:
            message = f.read()
        self.wfile.write(bytes(message, "utf8"))
        print('file served')

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
        print('_____query introduced is: %s ______' % full_query)
        return repos

    def list_drugs(self, limit = 10): # useful for drug_list, warning_list, company_list (just limit paremeter os requiered)
        # implements request by adding a limit parameter and call send_request to obtain the corresponding Json list
        request_ending = "limit=%s" % (limit)
        json_list = self.send_query(request_ending)
        print('_____json list has been returned: parameters: limit = %s______' % limit)
        return json_list

    def search_drugs(self, active, limit = 10): # useful for active_ingredient
        # implements request by adding an active_ingredient and a limit parameter to obtain the corresponding Json list
        request_ending = "search=active_ingredient:%s&limit=%s" % (active, limit)
        json_list = self.send_query(request_ending)
        print('_____json list has been returned: parameters: active = %s , limit = %s ______' % (active, limit))
        return json_list

    def search_companies(self, manufacturer, limit = 10):  # searches for manufacturer_name / returns brand_name
        # implements request by adding a manufacturer_name and limit parameter to obtain the corresponding Json list
        request_ending = "search=openfda.manufacturer_name:%s&limit=%s" % (manufacturer, limit)
        json_list = self.send_query(request_ending)
        print('_____json list has been returned: parameters: manufacturer = %s , limit = %s ______' % (manufacturer, limit))
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
                        warning_list.append("NOT FOUND")
                        break
            except KeyError:
                warning_list.append("NOT FOUND")
                continue
        return warning_list

    def parse_companies(self): # useful for manufacturer_list
        # called to return a list containing manufacturers
        manufacturer_list = []
        for i in range(len(repos['results'])):
            try:
                for n in range(len(repos['results'][i]["openfda"]["manufacturer_name"])):
                    try:
                        manufacturer_list.append(repos['results'][i]["openfda"]["manufacturer_name"])
                    except KeyError:
                        break
            except KeyError:
                manufacturer_list.append("NOT FOUND")
                continue
        return manufacturer_list


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        path = self.path

        if path != "/favicon.ico": # unnecessary
            print("PATH: path introduced by client:", path)

        if path == "/": # default
            print("SEARCH: client entered default search web")
            filename = "search.html"

        elif path.find('searchDrug') != -1:  # let´s try to find a drug and a limit entered by user
            try:
                print("SEARCHED: client has attemped to make a request")
                active = path.split("=")[1].split("&")[0]  # drug entered by client
                limit = path.split("=")[2]  # limit entered by client
                print("REQUEST: Client asked for drugs with %s and especified a limit of %s" % (active, limit))
                active_fda(active, limit)
                print("SUCCESS: Client has succesfully made a request")
                filename = "fda_info_tobesent.html"
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
                filename = "error.html"
        elif path.find('searchCompany') != -1:  # let´s try to find a manufacturer and a limit entered by user
            try:
                print("SEARCHED: Client searched for a manufacturer")  # this a check point
                manufacter = path.split("=")[1].split("&")[0] # drug entered by client
                limit = path.split("=")[2]  # limit entered by client
                print("REQUEST: Client asked for drugs produced by %s and especified a limit of %s" % (manufacter, limit))
                manufacturer_fda(manufacter, limit)
                filename = "fda_info_tobesent.html"
            except KeyError:
                print("BAD REQUEST: client has failed to make a request")
                filename = "error.html"
        elif path.find('listDrugs') != -1:  # let´s try to find a manufacturer and a limit entered by user
            try:
                print("Client searched for a list of drugs")  # this a check point
                limit = path.split("=")[1].split("&")[0]  # limit entered by client
                print("Client asked for a drug list and specified a limit of %s" % (limit))
                drugs_fda(limit)
                filename = "fda_info_tobesent.html"
            except KeyError:
                print("***** some ERROR occurred")
                filename = "error.html"
        elif path.find('listCompanies') != -1:  # let´s try to find a manufacturer and a limit entered by user
            try:
                print("Client searched for a list of manufacturers")  # this a check point
                limit = path.split("=")[1].split("&")[0]  # limit entered by client
                print("Client asked for a manufacturer list and especified a limit of %s" % (limit))
                manufacturers_fda(limit)
                filename = "fda_info_tobesent.html"
            except KeyError:
                print("***** some ERROR occurred")
                filename = "error.html"
        elif path.find('listWarnings') != -1:  # let´s try to find a manufacturer and a limit entered by user
            try:
                print("Client searched for a list of warnings")  # this a check point
                limit = path.split("=")[1].split("&")[0]  # limit entered by client
                print("Client asked for a warning list and especified a limit of %s" % (limit))
                drug_warning(limit)
                filename = "fda_info_tobesent.html"
            except KeyError:
                print("***** some ERROR occurred")
                filename = "error.html"
        else:
            if path != "/favicon.ico":
                print("***** ERROR: standard error")
            filename = "error.html"
            # Send message back to client

        if path != "/favicon.ico":
            send_file(filename)
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

