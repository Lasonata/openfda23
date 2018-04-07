# A simple web server using sockets
import socket
import http.client
import json

# Server configuration
current_ip = "192.168.1.109"
IP = current_ip # "127.0.0.1" # "10.3.52.67"
PORT = 8000 # not to be changed: teacher especified port to be 8000
MAX_OPEN_REQUESTS = 5

# we first define the actions (functions) our server can do:

def active_fda(active, limit): # searches for active_ingredient / returns brand name

    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?search=active_ingredient:%s&limit=%s" % (active,limit), None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()

    repos = json.loads(repos_raw)

    with open("fda_info_tobesent.html", "w") as f:
        f.write('<html><head><h1>Here you are:<title>Kwik-E-Mart</title></h1><body style="background-color: orange">\n<ol>')
        for i in range(len(repos['results'])):
            try:
                drug = repos['results'][i]["openfda"]["brand_name"][0]
                f.write('\n<li>')
                f.write(' brand name is: ')
                f.write(drug)
                f.write('</li>')
            except KeyError:
                f.write('\n<li>')
                f.write(' brand name is: ')
                f.write('NOT FOUND')
                f.write('</li>')
                continue
        f.write(
            '</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Apu Nahasapeemapetilon"><p><a href="http://%s:%s/">Back to Main Page</a></p></head></html>' %(current_ip, PORT))
        f.close()

def manufacturer_fda(manufacturer, limit): # searches for manufacturer_name / returns brand_name

    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?search=openfda.manufacturer_name:%s&limit=%s" % (manufacturer,limit), None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()

    repos = json.loads(repos_raw)

    with open("fda_info_tobesent.html", "w") as f:
        f.write('<html><head><h1>Here you are:<title>Kwik-E-Mart</title></h1><body style="background-color: orange">\n<ol>')
        for i in range(len(repos['results'])):
            try:
                drug = repos['results'][i]["openfda"]["brand_name"][0]
                f.write('\n<li>')
                f.write(' brand name is: ')
                f.write(drug)
                f.write('</li>')
            except KeyError:
                f.write('\n<li>')
                f.write(' brand name is: ')
                f.write('NOT FOUND')
                f.write('</li>')
                continue
        f.write(
            '</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Apu Nahasapeemapetilon"><p><a href="http://%s:%s/">Back to Main Page</a></p></head></html>' %(current_ip, PORT))
        f.close()

def drugs_fda(limit): # returns a drug list

    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=%s" % (limit), None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()

    repos = json.loads(repos_raw)

    with open("fda_info_tobesent.html", "w") as f:
        f.write('<html><head><h1>Here you are:<title>Kwik-E-Mart</title></h1><body style="background-color: orange">\n<ol>')
        for i in range(len(repos['results'])):
            try:
                drug = repos['results'][i]["openfda"]["brand_name"][0]
                f.write('\n<li>')
                f.write(' brand name is: ')
                f.write(drug)
                f.write('</li>')
            except KeyError:
                f.write('\n<li>')
                f.write(' brand name is: ')
                f.write("NOT FOUND")
                f.write('</li>')
                continue
        f.write(
            '</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Apu Nahasapeemapetilon"><p><a href="http://%s:%s/">Back to Main Page</a></p></head></html>' %(current_ip, PORT))
        f.close()

def manufacturers_fda(limit): # returns a company list

    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=%s" % (limit), None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()

    repos = json.loads(repos_raw)

    with open("fda_info_tobesent.html", "w") as f:
        f.write('<html><head><h1>Here you are:<title>Kwik-E-Mart</title></h1><body style="background-color: orange">\n<ol>')
        for i in range(len(repos['results'])):
            try:
                manufacturer = repos['results'][i]["openfda"]["manufacturer_name"]
                f.write('\n<li>')
                f.write(' company name is: ')
                f.write(manufacturer)
                f.write('</li>')
            except KeyError:
                f.write('\n<li>')
                f.write(' company name is: ')
                f.write("NOT FOUND")
                f.write('</li>')
                continue
        f.write(
            '</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Apu Nahasapeemapetilon"><p><a href="http://%s:%s/">Back to Main Page</a></p></head></html>' %(current_ip, PORT))
        f.close()

# define function to get the client request and act accordingly:

def process_client(clientsocket):
    """Function for attending the client. It reads their request message and
       sends the response message back, with the requested html content"""

    # Read the request message. It comes from the socket
    # What are received are bytes. We will decode them into an UTF-8 string
    request_msg = clientsocket.recv(1024).decode("utf-8")

    # Split the message into lines and remove the \r character
    request_msg = request_msg.replace("\r", "").split("\n")

    # Get the request line
    request_line = request_msg[0]

    # Break the request line into its components
    request = request_line.split(" ")

    # Get the two component we need: request cmd and path
    try:
        req_cmd = request[0]
        path = request[1]

        print("")
        print("REQUEST:", request_msg)
        print("Command: {}".format(req_cmd))
        print("Path: {}".format(path))
        print("")
    except IndexError:
        filename = "error.html"
        path = "error: not found... html file to send automatically set to error.html"

    # chooses the html page to send, depending on the path

    if path == "/" :
        filename = "search.html"

    elif path.find('active') != -1 : # let´s try to find a drug and a limit entered by user
        try:
            print("Client searched for an active ingredient") # this a check point
            activeloc = path.find('activo')  # finds drug location
            limitloc = path.find('limit')  # finds limit location
            active = path[activeloc + 7:limitloc - 1]  # drug entered by client
            limit = path[limitloc + 6:] # limit entered by client
            print("Client asked for drugs with %s and especified a limit of %s" % (active, limit))
            active_fda(active, limit)
            filename = "fda_info_tobesent.html"
        except KeyError:
            print("***** some ERROR occurred")
            filename = "error.html"
    elif path.find('manufacturer') != -1 : # let´s try to find a manufacturer and a limit entered by user
        try:
            print("Client searched for a manufacturer") # this a check point
            manufacturerloc = path.find('manufactorizador')  # finds drug location
            limitloc = path.find('limit')  # finds limit location
            manufacter = path[manufacturerloc + 17:limitloc - 1]  # drug entered by client
            limit = path[limitloc + 6:] # limit entered by client
            print("Client asked for drugs produced by %s and especified a limit of %s" % (manufacter, limit))
            manufacturer_fda(manufacter, limit)
            filename = "fda_info_tobesent.html"
        except KeyError:
            print("***** some ERROR occurred")
            filename = "error.html"
    elif path.find('druglist') != -1 : # let´s try to find a manufacturer and a limit entered by user
        try:
            print("Client searched for a list of drugs") # this a check point
            limitloc = path.find('limit')  # finds limit location
            limit = path[limitloc + 6:] # limit entered by client
            print("Client asked for a drug list and especified a limit of %s" % (limit))
            drugs_fda(limit)
            filename = "fda_info_tobesent.html"
        except KeyError:
            print("***** some ERROR occurred")
            filename = "error.html"
    elif path.find('manufacturerlist') != -1 : # let´s try to find a manufacturer and a limit entered by user
        try:
            print("Client searched for a list of manufacturers") # this a check point
            limitloc = path.find('limit')  # finds limit location
            limit = path[limitloc + 6:] # limit entered by client
            print("Client asked for a manufacturer list and especified a limit of %s" % (limit))
            manufacturers_fda(limit)
            filename = "fda_info_tobesent.html"
        except KeyError:
            print("***** some ERROR occurred")
            filename = "error.html"

    else:
        print("** standard error") # this a check point
        filename = "error.html"

    print("File to send: {}".format(filename))

    with open(filename, "r") as f:
        content = f.read()

    # Build the HTTP response message. It has the following lines
    # Status line
    # header
    # blank line
    # Body (content to send)

    # -- Everything is OK
    status_line = "HTTP/1.1 200 OK\n"

    # -- Build the header
    header = "Content-Type: text/html\n"
    header += "Content-Length: {}\n".format(len(str.encode(content)))

    # -- Busild the message by joining together all the parts
    response_msg = str.encode(status_line + header + "\n" + content)
    clientsocket.send(response_msg)

# -----------------------------------------------
# ------ The server start its executiong here
# -----------------------------------------------

# Create the server cocket, for receiving the connections
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    # Give the socket an IP address and a Port
    serversocket.bind((IP, PORT))

    # This is a server socket. It should be configured for listening
    serversocket.listen(MAX_OPEN_REQUESTS)

    # Server main loop. The server is doing nothing but listening for the
    # incoming connections from the clientes. When there is a new connection,
    # the systems gives the server the new client socket for communicating
    # with the client
    while True:
        # Wait for connections
        # When there is an incoming client, their IP address and socket
        # are returned
        print("Waiting for clients at IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        # Process the client request
        print("  Client request recgeived. IP: {}".format(address))
        print("Server socket: {}".format(serversocket))
        print("Client socket: {}".format(clientsocket))
        process_client(clientsocket)
        clientsocket.close()

except socket.error:
    print("Socket error. Problemas with the PORT {}".format(PORT))
    print("Compruebe IP")
