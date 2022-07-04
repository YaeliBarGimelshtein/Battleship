import socket

HEADER = 64  # each message will have a header to tell the message size
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" # when receiving, close the connection and disconnect client
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

# creating the socket so that it gets ip's and it is streaming data through it
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server
client.connect(ADDRESS)


def send(msg):
    """
    sends a message to the server through the socket
    :param msg: a string message to send to the server
    :return: void
    """
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER-len(send_lenght))  # padd to 64 bytes
    client.send(send_lenght)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


send("hello world!")
input()  # enter to go to next message
send("hello everyone!")
input()
send("hello Ran!")
input()
send(DISCONNECT_MESSAGE)