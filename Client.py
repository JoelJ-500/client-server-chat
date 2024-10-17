from socket import *
import datetime

class Client:
    # Establish connection through handshake
    '''DESIGN NOTE: In a real world application the client object will probably be 
    invoked from another object, hence it makes sense to establish a connection
    to server only when the client object is constructed
    '''
    def __init__(self):
        self.server_ip = '127.0.1.1'  # Run: 'wsl hostname -I' in powershell to get IP
        self.server_port = 12000  # Set in server file
        self.clientSocket = self.establish_connection()

    # Returns a socket that has communication with the specified server above
    ''' DESIGN NOTE: Having a function that creates a socket allows us to recreate a socket
        outside of initialization, in the event it is needed again after the connection is closed.
    '''
    def establish_connection(self):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        try:
            clientSocket.connect((self.server_ip, self.server_port))
            response = clientSocket.recv(1024).decode()
            if response == "max_cap": # If server already has 3 clients
                print("Server has reached max capacity of 3 clients. Try later")
                return None
            else:
                print("Connection established")
        except Exception as e:  
            print(f"Failed to connect: {e}")
            return None
        return clientSocket

    # Send a string to the server, get input through CLI
    def send_message(self, message):
        if self.clientSocket:  # Check if the socket is still open
            self.clientSocket.send(message.encode())
            # Get ack from server
            ack = self.clientSocket.recv(1024).decode()  # Decode acknowledgment
            if ack == message + "ACK":
                print("Message delivery is a success!")
                print(f"Acknowledgement Response: {ack}\n")

    # Send a 'status' message to receive server cache info
    def get_cache(self):
        if self.clientSocket:  # Check if the socket is still open
            self.clientSocket.send("status".encode())
            status = self.clientSocket.recv(1024).decode()  # Decode response
            return status

    # Send 'exit' message to close connection whenever user is ready
    def close_connection(self):
        if self.clientSocket:  # Check if the socket is still open
            self.clientSocket.send("exit".encode())
            self.clientSocket.close()  # Close socket after sending exit
            self.clientSocket = None  # Set to None to prevent further use

    # Send 'list' message. When list of files is received, ask user for name of file they want.
    # If entered file name is invalid, ask user again.
    def get_file(self):
        self.clientSocket.send("list".encode())

        # Print received file names
        files = self.clientSocket.recv(10000).decode().split(',')
        print(f"Files in server directory:\n" + '\n'.join(files))
        f_name = input("Select the file name you want (Must be case sensitive): ")

        while((f_name) not in files):
            f_name = input("File doesn't exist please try again!: ")
        
        # Send file name to server
        self.clientSocket.send(f_name.encode())

        response = self.clientSocket.recv(1024).decode()
        if response == "SENDING_FILE":
            # Receive the file size
            file_size = int(self.clientSocket.recv(1024).decode())
            print(f"Receiving file of size {file_size} bytes.")

            with open("received_file", 'wb') as f:
                bytes_received = 0
                while bytes_received < file_size:
                    bytes_read = self.clientSocket.recv(1024)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    bytes_received += len(bytes_read)

            print("File received successfully.")

    def get_name(self):
        name = self.clientSocket.send("get_name".encode())
        return self.clientSocket.recv(1024).decode()

if __name__ == "__main__":
    client = Client()
    if (not client.clientSocket): # Connection rejected
        exit() # Terminate program
    print(f"You are {client.get_name()}")
    print("Options:")
    print("'exit' : Close connection with server")
    print("'status' : Get client cache info")
    print("'list': request any file from the server.")

    print()
    print("\nAny other input than the above will be considered a message\n")
    while True:
        usr_input = input("\n")
        if usr_input == "exit":
            client.close_connection()
            break
        elif usr_input == "status":
            print(client.get_cache())
            continue
        elif usr_input == "list":
            client.get_file()  
        else:
            client.send_message(usr_input)

    print("\nClient shut down")
