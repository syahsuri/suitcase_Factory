import socket
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 5050))
server_socket.listen(1)
print("Server is listening...")
(client_socket, client_address) = server_socket.accept()
while True:
    received_msg = client_socket.recv(1024)
    print(f"Received message: {received_msg}")
    what_to_send = 'Ik verstond: ' + received_msg.decode()
    client_socket.send(what_to_send.encode())
client_socket.close()
server_socket.close()