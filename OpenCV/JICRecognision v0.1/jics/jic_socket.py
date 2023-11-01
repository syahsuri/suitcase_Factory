# File: jic_socket.py 

# JIC libraries
import socket

# Define socket
my_socket = None

# Initialize
def initialize():
    global my_socket
    log("Initializing...")

    my_socket = connect_to_server()

    log("Ready")
 
# Connect to server
def connect_to_server():
    global my_socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(('127.0.0.1', 10000))
    return my_socket

# Send data
def send_message(message):
    global my_socket
    my_socket.send(message.encode())
    log(f"Data sent [{message}]")

# Wait and receive data
def receive_message():
    global my_socket
    data = my_socket.recv(1024)
    log(f"Data received [{data.decode()}]")
    return data.decode()

# Close connection
def close():
    global my_socket
    my_socket.close()
    log("Connection closed")

# Check if stream is ready
def is_ready():
    global my_socket
    #if my_socket.connected:
    #    return True
    #return False
    return True

# Log messages in console
def log(message):
    print(f"JIC_Socket: {message}")