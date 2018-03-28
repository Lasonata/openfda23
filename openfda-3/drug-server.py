# A simple web server using sockets
import socket
import datetime

# Server configuration
IP = "192.168.1.109" # remember to change also link in html_file.html # before: 127.0.0.1
PORT = 9008
MAX_OPEN_REQUESTS = 5

import http.client
import json

def process_client(clientsocket):
    """Function for attending the client. It reads their request message and
       sends the response message back, with the requested html content"""

    # Read the request message. It comes from the socket
    # What are received are bytes. We will decode them into an UTF-8 string
    request_msg = clientsocket.recv(1024).decode("utf-8") # recieves up to 1024 bites and decodes them for sintax reading

    # Split the message into lines and remove the \r character
    request_msg = request_msg.replace("\r", "").split("\n") # here the client especify its request

    # Get the request line
    request_line = request_msg[0] # # here we leave only the first line of client request

    # Break the request line into its components
    request = request_line.split(" ")

    # Get the two component we need: request cmd and path
    try: # in case path = request[1] causes: <<IndexError: list index out of range>>
        req_cmd = request[0] # GET
        path = request[1] # after slash (/) --> cient especific request
        print("")
        print("REQUEST: ")
        print("Command: {}".format(req_cmd))
        print("Path: {}".format(path))
        print("Time: ", datetime.datetime.now())
        print("")
    except IndexError: # this was made to solve a recurrent error in which the path was empty and so, request[1] caused an index error
        print('ERROR: path not found') # just an error message: code will not work anyways
        path = 'error' # we assign anythin to path so that it doesnt rise an error and the html file returned is error.html
        print('NOTE: path automatically assigned to error.html file as default')
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov") # main page we search
    conn.request("GET", "/drug/label.json?limit=10", None, headers) # specific page we search
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()

    repos = json.loads(repos_raw) # web page info for sintax reading

    # let's try to write them down in an html file
    table_file = open('html_file_2.html', 'w')
    table_file.write('<html><head><h1>Here you are:</h1><body style="background-color: yellow">\n<ol>')
    for i in range(len(repos['results'])):
        drug = repos['results'][i]["id"]
        table_file.write('\n<li>')
        table_file.write(' id is: ')
        table_file.write(drug)
        table_file.write('</li>')  # this will be removed when \n error is fixed
    table_file.write('</ol><h3>Thank you, come again</h3> \n <img src="http://www.konbini.com/en/files/2017/08/apu-feat.jpg" alt="Sad"><p><a href="http://192.168.1.109:9008/">Back to Main Page</a></p></head></html>')
    table_file.close()

    # Read the html page to send, depends on the path
    if path == "/":
        filename = "html_file.html"
        print('html file requested: html_file.html')
    elif path == "/10drugs":
        filename = "html_file_2.html"
        print('html file requested: html_file_2.html')
    else:
        filename = "error.html"
        print('html file requested does not exist')

    print("File to send: {}".format(filename))

    with open(filename, "r") as f: # opening especified html file
        content = f.read() #storing in content

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
    print("Compruebe la IP y el puerto")
