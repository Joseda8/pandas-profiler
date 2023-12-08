import socket

class Client:
    def __init__(self, host, port):
        """
        Initializes the Client object.

        Parameters:
            host (str): The IP address of the server.
            port (int): The port on which the client will connect to the server.
        """
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_message(self, message):
        """
        Sends a message to the server and receives a response.

        Parameters:
            message (str): The message to be sent to the server.
        """
        # Send message to the server
        self.client_socket.send(message.encode('utf-8'))

        # Receive response from the server
        _ = self.client_socket.recv(1024).decode('utf-8')

        # Close the connection
        self.client_socket.close()
