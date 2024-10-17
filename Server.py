from socket import *
import socket
import datetime
import threading
from pathlib import Path
import os

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
        self.server_socket = socket.socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', self.server_port))
        self.server_socket.listen(3)

        # Output server IP and port
        print(f"Server listening on {socket.gethostbyname(socket.gethostname())}:{self.server_port} ")

        # Create a shutdown server, thread event
        self.shutdown_event = threading.Event()

        # Listens and handles requests from clients
        while not self.shutdown_event.is_set():
            # Handle any handshake request
            connection_socket, addr = self.server_socket.accept()

            # Check if server at max capacity of 3 clients
            if (self.connected_clients >= 3):
                message = "max_cap"
                connection_socket.send(message.encode())
                continue
            else:
                message = "success"
                connection_socket.send(message.encode())
            # Create and start a new thread for said connection
            client_thread = threading.Thread(target=self.listen, args=(connection_socket, addr))
            client_thread.start()

        # Shuts down server, when loop above ends
        self.server_socket.close()

    # Listen for the type of request and handle accordingly
    def listen(self, connection_socket, addr):            
        # Add the client once handshake built, and get the name of client. 
        cname = self.add_client(addr, datetime.datetime.now().strftime("%B %d, %Y %I:%M %p"), connection_socket)

        while True:
            # Read the client message to determine what action to take
            message = connection_socket.recv(1024).decode()
            
            if message == "exit":
                self.close_connection(connection_socket, cname)
                break

            elif message == "status":
                self.send_status(connection_socket)

            elif message == "get_name":
                connection_socket.send(cname.encode())

            elif message == "list": 
                # Gives a list of files in server directory to client
                connection_socket.send(self.get_files().encode())
                # Recieve the file name the client requests
                f_name = connection_socket.recv(1024).decode()
                self.send_file(connection_socket, f_name)

            else: # handles recieved message
                self.echo_message(message, connection_socket)
                
             
    # Updates the clients and cache list attribute to add client
    # Returns the client name
    def add_client(self, addr, date_added, con_socket):
        self.num_clients += 1
        self.connected_clients += 1

        # Check if ip addr already exists in cache
        for client in self.cache:
            if client[1] == addr:
                self.cache.append([cname, addr, date_added, None])
                return client[0] #name of client with matching ip

        # Create a client name in format Client01, Client02, etc
        cname = "Client" + str(self.num_clients)

        # Add to clients list
        self.clients.append([cname, addr, con_socket])

        # Add to cache
        self.cache.append([cname, addr, date_added, None])

        return cname

    #  Echos a recived string message, back to client with 'ACK' appended at the end.
    def echo_message(self, message, connection_socket):
        message += str("ACK")
        connection_socket.send(message.encode())

    # Upon recieving an exit message, terminates the connection with the specified client.
    def close_connection(self, connection_socket, cname):
        if (self.connected_clients == 0): # Client doesn't exist
            return
        else: self.connected_clients -= 1

        connection_socket.close() # Close connection
        date_ended = datetime.datetime.now().strftime("%B %d, %Y %I:%M %p")

        # Add connection end time to connection cache
        for connection in self.cache:
            if connection[0] == cname:
                connection[len(connection)-1] = date_ended
                break

    # Return cache of specific client
    def send_status(self, con_socket):
        status = ''.join(str(item)+"\n" for item in self.cache)  # Convert each item to a string
        con_socket.send(status.encode())

    # Returns list of files on server
    def get_files(self):
        files = ""
        directory = Path('files/')

        for f in directory.iterdir():
            if f.is_file(): files += f.name + ","
        
        return files

    # Gives a requested file to client
    # If file doesn't exist inform client by returning 'dne'
    def send_file(self, con_socket, filename): #con_sock: socket of client
        # Notify the client to expect a file
        con_socket.send("SENDING_FILE".encode())

        # Add dir to filename
        filename = "files/"+filename

        # Send the file size
        file_size = os.path.getsize(filename)
        con_socket.send(f"{file_size}".encode())

        # Open the file and send its content
        with open(filename, 'rb') as f:
            bytes_read = f.read(1024)
            while bytes_read:
                con_socket.send(bytes_read)
                bytes_read = f.read(1024)

        print("File sent successfully.")

if __name__ == "__main__":
    server = Server()
