from socket import *
import datetime

class Server:
    def __init__(self):
        self.server_port = 12000 # Set server port

        self.num_clients = 0 # Total clients connected
        self.connected_clients = 0 # Amt of connected clients

        # Set up cache in the form of 2d list
        # Format: [ [client_name, time & date connection started, time & date connection ended]  ]
        self.cache = []

        # List for tracking clients and their ip 
        # Format: [[client name, ip]]
        self.clients = []

        # Set up welcoming socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', self.server_port))
        self.server_socket.listen(1)

        # Listens and handles requests from clients
        self.listen()

        self.server_socket.close()

    # Listen for the type of request and handle accordingly
    def listen(self):
        while True:
            # Handle handshake request
            connection_socket, addr = self.server_socket.accept()
            if not(self.connected_clients < 3): # If 3 clients are already connected reject connection
                connection_socket.close()
                continue
            else:
                date_added = datetime.datetime.now()
            
            # Add the client once handshake built, and get the name of client. 
            cname = self.add_client(addr, date_added)

            # Read the client message to determine what action to take
            message = connection_socket.recv(1024).decode()

            if message == "exit":
                self.close_connection(connection_socket, cname)
            elif message == "shutdown": # End session
                break
                #NOTE: We don't have to close every clients connection,
                #  as closing the server socket automatically does it for us.
                # and since the session data is only temporary we dont have to write the end times
                # of every connection we close, making closing every connection redundant
            else:
                self.echo_message(message, connection_socket)
                
             
    # Updates the clients and cache list attribute to add client
    # Returns the client name
    def add_client(self, addr, date_added):
        self.num_clients += 1
        self.connected_clients += 1

        # Create a client name in format Client01, Client02, etc
        cname = "Client" + str(self.num_clients)

        # Add to clients list
        self.clients.append([cname, addr])

        # Add to cache
        self.cache.append([cname, date_added, None])

        return cname

    #  Echos a recived string message, back to client with 'ACK' appended at the end.
    def echo_message(self, message, connection_socket):
        connection_socket.send(message+"ACK".encode())

    # Upon recieving an exit message, terminates the connection with the specified client.
    def close_connection(self, connection_socket, cname):
        if (self.connected_clients == 0): # Client doesn exist
            return
        else: self.connected_clients -= 1

        connection_socket.close() # Close connection
        date_ended = datetime.datetime.now()

        # Add connection end time to connection cache
        for connection in self.cache:
            if connection[0] == cname:
                connection[2] = date_ended
                break

    # Listen for a 'list' message. Upon recieval, give a list of files, and wait for response.
    # Upon response send the clients desired file. If name invalid ask again.

if __name__ == "__main__":
    server = Server()
