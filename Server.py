from socket import *
import datetime

class Server:
    def __init__(self):
        self.server_port = 12000 # Set server port

        self.num_clients = 0 # Amt of connected clients

        # Set up cache in the form of 2d list
        # Format: [ [client_name, time & date connection started, time & date connection ended]  ]
        self.cache = []; 

        # List for tracking clients and their ip 
        # Format: [[client name, ip]]
        self.clients = []

        # Set up welcoming socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', self.server_port))
        self.server_socket.listen(1)

        # Listens and handles requests from clients
        self.listen()

    # Listen for the type of request and handle accordingly
    def listen(self):
        while True:
            # Handshake request
            connection_socket, addr = self.server_socket.accept()
            if not(self.num_clients < 3): # If 3 clients are already connected reject connection
                connection_socket.close()
                continue
            else:
                date_added = datetime.datetime.now()
            
            # Add the client once handshake built
            self.add_client(addr, date_added)
             
    # Updates the clients and cache list attribute to add client
    def add_client(self, addr, date_added):
        self.num_clients += 1

        # Create a client name in format Client01, Client02, etc
        cname = "Client0" + str(self.num_clients)

        # Add to clients list
        self.clients.append([cname, addr])

        # Add to cache
        self.cache.append([cname, date_added, None])

    # Listen for any tcp messages with a string. Once recived echo same string back to client
    # with 'ACK' appended at the end. 

    # Listen for an 'exit' message. Upon recieval, terminate connection with that specific client.

    # Listen for a 'list' message. Upon recieval, give a list of files, and wait for response.
    # Upon response send the clients desired file. If name invalid ask again.

if __name__ == "__main__":
    server = Server()
