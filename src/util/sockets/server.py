import socket
import time

class Server:
    def __init__(self, host, port):
        """
        Initializes the Server object.

        Parameters:
            host (str): The IP address of the server.
            port (int): The port on which the server will listen for connections.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_socket()

    def bind_socket(self):
        """Binds the server socket to the specified host and port with retry."""
        while True:
            try:
                self.server_socket.bind((self.host, self.port))
                break
            except OSError as e:
                if e.errno == 98:  # Address already in use
                    print(f"Port {self.port} is still in use. Retrying in 1 second...")
                    time.sleep(1)
                else:
                    raise

        self.server_socket.listen(5)

    def stop_server(self):
        """Stops the server."""
        self.server_socket.close()

    def wait_for_message(self, expected_message):
        """
        Waits for a specific message from the client and sends a response.

        Parameters:
            expected_message (str): The expected message from the client.
        """
        client_socket, _ = self.server_socket.accept()

        # Receive message from the client
        received_message = client_socket.recv(1024).decode('utf-8')

        # Check if the received message matches the expected message
        if received_message == expected_message:
            response = "Message received successfully."
        else:
            response = "Unexpected message."

        # Send a response back to the client
        client_socket.send(response.encode('utf-8'))

        # Close the connection
        client_socket.close()
