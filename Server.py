import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
HEADER = 64  # each message will have a header to tell the message size
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" # when receiving, close the connection and disconnect client

# creating the socket so that it gets ip's and it is streaming data through it
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding the socket to an address - anything that is connected to this address will hit this socket
server.bind(ADDRESS)


def handle_client(port, ip):
    """
    handle individual connection between one client and the server
    :param port: client's port number of the connection
    :param ip: client's ip address
    :return: void
    """
    print(f"[NEW CONNECTION] {ip} connected.")
    connected = True
    while connected:
        msg_lenght = port.recv(HEADER).decode(FORMAT)  # blocks until receiving a message and convert it from bytes
        if msg_lenght:  # check not none
            msg_lenght = int(msg_lenght)
            msg = port.recv(msg_lenght).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{ip}] {msg}")
            port.send("msg received".encode(FORMAT))
    port.close()


def start():
    """
    start listening for new connections and handling them by passing them to the handle function -
     each connection gets a thread
    :return: void
    """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        port, ip = server.accept()  # blocks. waits for new connection to the server
        thread = threading.Thread(target=handle_client, args=(port, ip))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")  # one thread starts the program, so not include it


print("[STARTING] server is starting...")
start()
