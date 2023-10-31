# File: jic_socket.py

# Import libraries
import socket
import time
import select

# JIC libraries
from jic_settings import online_mode

# Define socket connection variable
my_socket = socket

ip_address = "127.0.0.1"
port = 10000
id = "2"

# Initialize socket connection
def initialize():
    global my_socket
    log("Initializing...")

    if(not online_mode):
        log("Offline mode")
        return
    my_socket = connect_to_server()
    if not is_connected():
        log("Failed")
        return

    log("Ready")

# Connect to socket server
def connect_to_server():
    log("Connecting to server...")
    global my_socket, ip_address, port
    server_address = (ip_address, port)

    while True:
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.connect(server_address)
            send_command(id)
            return my_socket
        except ConnectionRefusedError:
            log("Connection attempt failed. Retrying...")
            time.sleep(5)

# Send data over socket
def send_command(message):
    if(not online_mode):
        return
    global my_socket
    my_socket.send(message.encode())
    log(f"Data sent: {message}")


def wait_for_command(timeout=0.1):
    log("Waiting for command...")
    if not online_mode:
        log("Offline Mode: No commands")
        return

    global my_socket
    ready = select.select([my_socket], [], [], timeout)
    if ready[0]:
        data = my_socket.recv(1024).decode()
        if data:
            log(f"Command received: {data}")
            return data
    else:
        log("No command received within the timeout")
        return None

# Check if the socket is connected to the server
def is_connected():
    global my_socket
    if my_socket is not None:
        try:
            # Try to get the peer name, which will raise an exception if not connected
            peername = my_socket.getpeername()
            return True
        except OSError:
            pass
    return False

# Close socket connection
def close():
    if(not online_mode):
        return
    global my_socket
    my_socket.close()
    log("Connection closed")

# Check if ready
def is_ready():
    if(not online_mode or is_connected()):
        return True
    return False

# Log messages in console
def log(message):
    print(f"JIC_Socket: {message}")