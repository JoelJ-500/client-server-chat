from socket import *
import datetime
import threading

class Server:
    def __init__(self):
        self.server_port = 12000 # Set server port

        self.num_clients = 0 # Total clients connected
        self.connected_clients = 0 # Number of active connections

        # Set up cache in the form of 2d list
        # Format: [ [client_name, time & date connection started, time & date connection ended]  ]
        self.cache = []

        # List for tracking clients and their ip 
        # Format: [[client name, ip, client socket]]
        self.clients = []

        # Set up welcoming socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', self.server_port))
        self.server_socket.listen(3)

        # Create a shutdown server, thread event
        self.shutdown_event = threading.Event()

        # Listens and handles requests from clients
        while not self.shutdown_event.is_set():
            # Handle any handshake request
            connection_socket, addr = self.server_socket.accept()
            # Create and start a new thread for said connection
            client_thread = threading.Thread(target=self.listen, args=(connection_socket, addr))
            client_thread.start()

        # Shuts down server, when loop above ends
        self.server_socket.close()

    # Listen for the type of request and handle accordingly
    def listen(self, connection_socket, addr):            
        # Add the client once handshake built, and get the name of client. 
        cname = self.add_client(addr, datetime.datetime.now(), connection_socket)

        # Read the client message to determine what action to take
        message = connection_socket.recv(1024).decode()

        if message == "exit":
            self.close_connection(connection_socket, cname)
        elif message == "shutdown": # End session
            for client in self.clients:
                client_sock = client[2]
                client_sock.close()
            self.shutdown_event.set()
            # NOTE: Since the session data is only temporary we dont have to write the end times
            # of every connection we close during shutdown.
        else:
            self.echo_message(message, connection_socket)
                
             
    # Updates the clients and cache list attribute to add client
    # Returns the client name
    def add_client(self, addr, date_added, con_socket):
        self.num_clients += 1
        self.connected_clients += 1

        # Create a client name in format Client01, Client02, etc
        cname = "Client" + str(self.num_clients)

        # Add to clients list
        self.clients.append([cname, addr, con_socket])

        # Add to cache
        self.cache.append([cname, date_added, None])

        return cname

    #  Echos a recived string message, back to client with 'ACK' appended at the end.
    def echo_message(self, message, connection_socket):
        connection_socket.send(message+"ACK".encode())

    # Upon recieving an exit message, terminates the connection with the specified client.
    def close_connection(self, connection_socket, cname):
        if (self.connected_clients == 0): # Client doesn't exist
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
