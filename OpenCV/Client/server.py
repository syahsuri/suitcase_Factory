import asyncio
import socket

# Define the server address and port
ip_address = ""
port = 10000

# Define a list to keep track of connected clients
clients = {}

# Start server
def start_server():
    print("Initializing...")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(5)

    print("Server is online")
    return server_socket

async def broadcast(message, not_to_client = None):
    print(f"Server to All: {message}")
    for client in clients:
        if not client == not_to_client:
            client.send((f"{message}").encode())
    
async def send_message(client, message):
    print(f"Server to Client [{clients[client]}]: {message}")
    client.send((f"{message}").encode())

async def incoming_message(client, message):
    print(f"Client [{clients[client]}] to Server: {message.decode()}")
    await broadcast(message.decode(), client)

async def client_connected(client):
    client_id = (await loop.sock_recv(client, 1024)).decode().strip()
    clients[client] = client_id
    print(f"Client [{client_id}] connected")

def client_disconnected(client):
    client.close()
    if client in clients:
        client_id = clients[client]
        del clients[client]
        print(f"Client [{client_id}] disconnected")

async def handle_client(client):    
    try:
        await client_connected(client)
        while True:
            try:
                data = await loop.sock_recv(client, 1024)
                if not data:
                    break
                await incoming_message(client, data)
            except ConnectionResetError:
                break
    except asyncio.CancelledError:
        pass
    finally:
        client_disconnected(client)
        

async def main():
    server_socket = start_server()
    print("Waiting for clients...")

    while True:
        client, address = await loop.sock_accept(server_socket)
        asyncio.create_task(handle_client(client))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())