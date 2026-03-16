import socket
import threading

HOST = "127.0.0.1"
PORT = 4100

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

print("Server started...")

# OSI Layer logging for messages
def log_osi_layers_send(message, client):
    print("\n--- Sending Message Through OSI Layers ---")
    print(f"[Application Layer] Message to broadcast: {message.decode()}")
    print("[Presentation Layer] Message is already bytes")
    print("[Session Layer] Maintaining session with client")
    print("[Transport Layer] Sending via TCP socket")
    print(f"[Network Layer] Destination IP {client.getpeername()[0]}, Port {client.getpeername()[1]}")
    print("[Data Link Layer] Framing the message")
    print("[Physical Layer] Signal transmitted\n")

def broadcast(message):
    for client in clients:
        log_osi_layers_send(message, client)
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            print("\n--- Receiving Message Through OSI Layers ---")
            print(f"[Physical Layer] Signal received")
            print("[Data Link Layer] Frame received and checked")
            print("[Network Layer] IP and Port checked")
            print("[Transport Layer] TCP segment received")
            print("[Session Layer] Session active")
            print("[Presentation Layer] Decoding bytes to text")
            print(f"[Application Layer] Message: {message.decode()}\n")

            broadcast(message)

            # Auto reply
            if b"hi" in message.lower():
                broadcast(b"Server: hi")

        except:
            if client in clients:
                index = clients.index(client)
                username = usernames[index]

                clients.remove(client)
                usernames.remove(username)

                broadcast(f"{username} left the chat".encode())
                client.close()
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send(b"USERNAME")
        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        print("Username:", username)
        broadcast(f"{username} joined chat".encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()