import socket
import threading
import random
import numpy as np
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
HEADER = 64  # each message will have a header to tell the message size
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"  # when receiving, close the connection and disconnect client
GET_BOARD_MESSAGE = "GET_BOARD"


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
        self.player1_board = [[]]
        self.player1_ships = []
        self.ships_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

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
                elif msg == GET_BOARD_MESSAGE:
                    ships_positions =self.create_battleground()
                    print("board created!")
                    for i in ships_positions:
                        points = []
                        points.extend(list(i[0]))
                        points.extend(list(i[1]))
                        msg_to_send = str(points).encode(FORMAT)
                        print(''.join(msg_to_send.decode(FORMAT)))
                        #msg_to_send = np.array(self.create_battleground()).tobytes()
                        msg_lenght = len(msg_to_send)
                        send_lenght = str(msg_lenght).encode(FORMAT)
                        send_lenght += b' ' * (HEADER - len(send_lenght))  # pad to 64 bytes
                        port.send(send_lenght)  # send header
                        port.send(msg_to_send)  # send msg
                print(f"[{ip}] {msg}")
                # port.send("msg received".encode(FORMAT))

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
        self.player1_board = self.init_board(self.player1_board)
        for size in self.ships_sizes:
            self.add_ship_to_board(size, self.player1_board, self.player1_ships)
        print(self.player1_ships)
        print(len(self.player1_ships))
        return self.player1_ships

    def get_random_location(self):
        x = random.randint(0, self.board_size - 1)
        y = random.randint(0, self.board_size - 1)
        return (x, y)

    def add_ship_to_board(self, size, board, ships):
        location = self.get_random_location()
        while (not self.try_place_ship(location, size, board, ships)):
            location = self.get_random_location()
        return

    def init_board(self, board):
        board = [[0 for x in range(self.board_size)] for y in range(self.board_size)]
        return board

    def try_place_ship(self, location, size, board, ships):
        start_x, end_x, start_y, end_y = location[0], location[0], location[1], location[1]
        direction = random.randint(0, 3)
        i = 0
        while (i < 5):
            if direction == 0:  # check for left direction
                if location[0] - size < 0:
                    direction = i
                    i += 1
                    continue
                start_x = location[0] - size
                if self.is_valid_location(start_x, end_x, start_y, end_y, board, ships):
                    return True
            elif direction == 1:  # check for right direction
                if location[0] + size >= self.board_size:
                    direction = i
                    i += 1
                    continue
                end_x = location[0] + size
                if self.is_valid_location(start_x, end_x, start_y, end_y, board, ships):
                    return True
            elif direction == 2:  # check for up durection
                if location[1] - size < 0:
                    direction = i
                    i += 1
                    continue
                start_y = location[1] - size
                if self.is_valid_location(start_x, end_x, start_y, end_y, board, ships):
                    return True
            elif direction == 3:
                if location[1] + size >= self.board_size:
                    direction = i
                    i += 1
                    continue
                end_y = location[1] + size
                if self.is_valid_location(start_x, end_x, start_y, end_y, board, ships):
                    return True

        return False

    def is_valid_location(self, start_x, end_x, start_y, end_y, board, ships):
        for x in range(start_x, end_x ):  # run over the location and check if has ships
            for y in range(start_y, end_y + 1):
                if board[x][y] == 1:
                    return False
        for x in range(start_x, end_x ):  # assign ship at the location
            for y in range(start_y, end_y + 1):
                self.player1_board[x][y] = 1
        ship = [(start_x, start_y), (end_x, end_y)]
        ships.append(ship)
        return True


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board)):
            print(board[i][j], end="")
        print()


class Ship():
    def __init__(self, size, start, end):
        self.lives = size
        self.start_x = start[0]
        self.start_y = start[1]
        self.end_x = end[0]
        self.end_y = end[1]

    def hit(self):
        self.lives -= 1


server = Server()
#server.create_battleground()
server.start()
