from socket import *

class Client:
    # Establish connection through handshake
    '''DESIGN NOTE: In a real world application the client object will probably be 
    invoked from another object, hence it makes sense to establish a connection
    to server only when the client object is constructed
    '''
    def __init__(self):
        self.server_ip = '172.20.152.221' # Run: 'wsl hostname -I' in powershell, to get IP
        self.server_port = 12000 # Set in server file
        self.clientSocket = self.establish_connection()

    # Returns a socket, that has communication with specified server above
    ''' DESIGN NOTE: Having a function that creates a socket, allows us to recreate a socket
        outside of initialization, in the event it is again needed after the connection is closed.
    '''
    def establish_connection(self):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        try:
            clientSocket.connect((self.server_ip, self.server_port))
            print("Connection established")
        except Exception as e: # If server already has 3 clients
            print(f"Failed to connect: Server is possibly full{e}")
            return None
        return clientSocket

    # When connection is accepted, communicate name back to server.

    # Send a string to the server, get input through CLI

    # Send a 'status' message to recieve, sever cache info 

    # Send 'exit' message, to close connection whenever user ready.

    # Send 'list' message. When list of files recieved, ask user for name of file they want.
    # If entered file name invalid ask user again.

if __name__ == "__main__":
    client = Client()