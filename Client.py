import socket
import pygame
from ClientGuiUtils import create_gui
import ClientCalcUtils

HEADER = 64  # each message will have a header to tell the message size
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"  # when receiving, close the connection and disconnect client
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)


class Client:
    """
    represents a client connecting to server and created gui
    """

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_rectangles = []
        self.opponent_rectangles = []
        grid = self.connect_to_server()
        self.gui(grid)

    def connect_to_server(self):
        """
        Initialize connection to server and get location of battleships
        :param self: the client
        :return: grid to create the board
        """
        self.socket.connect(ADDRESS)
        # TODO : get grid from server (2d int)
        grid = []
        for row in range(11):
            grid.append([])
            for column in range(11):
                grid[row].append(0)
        grid[4][5] = 1
        grid[4][6] = 1
        return grid

    def send(self, msg):
        """
        sends a message to the server through the socket
        :param msg: a string message to send to the server
        :return: void
        """
        message = msg.encode(FORMAT)
        msg_lenght = len(message)
        send_lenght = str(msg_lenght).encode(FORMAT)
        send_lenght += b' ' * (HEADER - len(send_lenght))  # pad to 64 bytes
        self.socket.send(send_lenght)
        self.socket.send(message)
        print(self.socket.recv(2048).decode(FORMAT))

    def gui(self, grid_from_server):
        """
        creates the gui for the game
        :param grid_from_server: ships location generated from the server
        :return: void
        """
        create_gui(grid_from_server, self.my_rectangles, self.opponent_rectangles)

    def handle_game(self):
        done = False
        while not done:
            # TODO : get message from server to make a move
            # TODO : get message from server to check opponent move
            # TODO : get message from server to get hit or miss
            # TODO : get message for win
            # TODO : get message for loose
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # mouse left button pressed
                    pos = pygame.mouse.get_pos()
                    x, y = ClientCalcUtils.check_rectangle_pressed(self.opponent_rectangles, pos)  # can be none
                    print(x, y)
                    if x is not None and y is not None:
                        self.send("TRY HIT " + str(x) + " " + str(y))

        pygame.quit()
        self.send(DISCONNECT_MESSAGE)


client = Client()
client.handle_game()
