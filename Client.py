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
            print("Connection established")
        except Exception as e:  # If server already has 3 clients
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
    def get_file(self, message):
        # Implement logic for requesting a file from the server
        pass

if __name__ == "__main__":
    client = Client()
    print("Options:")
    print("'exit' : Close connection with server")
    print("'status' : Get client cache info")
    print("'list': request any file from the server.")

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
            client.get_file(usr_input)  # Pass the message to get_file
        else:
            client.send_message(usr_input)

    print("\nClient shut down")
