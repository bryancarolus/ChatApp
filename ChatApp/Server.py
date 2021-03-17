from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# Constant Variables
HOST = ''
PORT = 5500
BUFSIZ = 512
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# Global Variables
clients = {}
addresses = {}


# Handles incoming clients
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome! Type your name and press Enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


# Handles a single client connection
def handle_client(client):
    try:
        name = client.recv(BUFSIZ).decode("utf8")
        welcome = "Welcome %s! To quit, type {quit} to exit." % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name

        while True:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name + ": ")
            else:
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                print(str(client))
                break
    except ConnectionResetError:
        print(str(client) + "ConnectionResetError")
    except OSError:
        print(str(client) + "OSError")


# Broadcast a message to all of the clients
def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SERVER.listen(10)  # Listens for 10 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
