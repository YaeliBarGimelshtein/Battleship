import socket
import threading
import random

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
HEADER = 64  # each message will have a header to tell the message size
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"  # when receiving, close the connection and disconnect client


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Server():

    def __init__(self):
        print("[STARTING] server is starting...")
        # creating the socket so that it gets ip's and it is streaming data through it
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # binding the socket to an address - anything that is connected to this address will hit this socket
        self.server.bind(ADDRESS)
        self.board_size = 10
        self.ships_sizes = [4,3,3,2,2,2,1,1,1,1]

    def handle_client(self, port, ip):
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

    def start(self):
        """
        start listening for new connections and handling them by passing them to the handle function -
         each connection gets a thread
        :return: void
        """
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            port, ip = self.server.accept()  # blocks. waits for new connection to the server
            thread = threading.Thread(target=self.handle_client, args=(port, ip))
            thread.start()
            print(
                f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")  # one thread starts the program, so not include it

    def create_battleground(self):
        self.player1_board = [[]]
        for size in range(self.ships_sizes):
            location = self.get_random_location()
            self.generate_ship(location,size)

    def get_random_location(self):
        x = random.randint(0, self.board_size - 1)
        y = random.randint(0, self.board_size - 1)
        return (x, y)

    def generate_ship(self, location,size):
        location =[-1,-1]
        while(not self.is_valid_location(location,size)):
            return 0
    def is_valid_location(self,location,size):
        for i in range(4):
           direction = random.randint(0,3)



class Ship():
    def __init__(self, size,location):
        self.lives = size

    def hit(self):
        self.lives-=1


server = Server()
serv = Server()
server.start()
