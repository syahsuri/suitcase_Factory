import socket

# Define the server address and port
server_address = ('', 10000)  # Listen on all available network interfaces

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections (max 1 pending connection)
server_socket.listen(1)

print("Waiting for a client to connect...")

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    
    print(f"Connected to client at {client_address}")
    
    # Send a message to the connected client
    message = "Hello, client! You are connected."
    client_socket.send(message.encode('utf-8'))
    
    # Close the client socket
    client_socket.close()