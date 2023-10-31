import socket
import asyncio

name_socket = "server"
server_socket = None

# Connect to server
# Returns True or False whether the connection has been made (attempts = 0 for not limit)
async def connect_to_server(attempts=0):
    global server_socket
    if is_connected_to_server():
        return True

    id = "1"
    port = 10000
    ip = "127.0.0.1"
    attempt = 0

    print("Attempting to connect...")
    while attempt < attempts or attempts == 0:
        if server_socket:
            send_command(id)
            print("Connected to server")
            return True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.connect((ip, port))
        except ConnectionRefusedError:
            pass
        attempt += 1
        await asyncio.sleep(1)
    return False

# Returns True or False whether it's connected to the server
def is_connected_to_server():
    return server_socket is not None

# Wait for command
# Returns False if not receiving command after timeout (timeout = 0 for no limit)
async def wait_for_command(timeout=0):
    if server_socket:
        if timeout == 0:
            return server_socket.recv(1024).decode()
        else:
            server_socket.settimeout(timeout)
            try:
                return server_socket.recv(1024).decode()
            except socket.timeout:
                return False
    else:
        return False

# Send command to server
# Returns True or False whether it sent the command. Retry = True will continue trying.
def send_command(command, retry=False):
    global server_socket
    if server_socket:
        try:
            server_socket.send(command.encode())
            return True
        except:
            server_socket = None
    if retry:
        asyncio.sleep(1)
        return send_command(command, retry)
    return False