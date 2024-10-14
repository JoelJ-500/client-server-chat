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
    def send_message(self, message):
        return

    # Send a 'status' message to recieve, sever cache info
    def get_cache(self):
        status = ""
        return status

    # Send 'exit' message, to close connection whenever user ready.
    def close_connection(self):
        return

    # Send 'list' message. When list of files recieved, ask user for name of file they want.
    # If entered file name invalid ask user again.
    def get_file(self, message):
        return

if __name__ == "__main__":
    client = Client()
    print("Options:")
    print("'exit' : Close connection with server")
    print("'status' : Get client cache info")
    print("'list': request any file, in server repo.")

    print("\n Any other input will be considered a message\n")
    input = ""
    while True:
        input = input("\n")
        if input == "exit":
            client.close_connection()
            break
        elif input == "status":
            print(client.get_cache)
            continue
        elif input == "list":
            client.get_file()
        else:
            client.get_message(input)

    print("Chat app shut down")