import json
import socket
import pygame
from ClientGuiUtils import create_gui, draw_text, draw_blink_rect
import ClientCalcUtils
import Ship
import sys

HEADER = 64  # each message will have a header to tell the message size
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"  # when receiving, close the connection and disconnect client
GET_BOARD_MESSAGE = "GET_BOARD"
GET_TURN_MESSAGE = "GET_TURN"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
BLINK_EVENT = pygame.USEREVENT + 0
YOUR_TURN = "Your turn, Select opponent battleship location"
OPPONENT_TURN = "Opponent Turn, please wait"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Client:
    """
    represents a client connecting to server and created gui
    """

    def __init__(self):
        self.args = sys.argv
        self.my_name = self.args[1]
        self.opponent_name = self.args[2]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_grid_rectangles = []
        self.opponent_rectangles = []
        self.ships = []
        self.screen = None
        self.ships_indexes, self.turn = self.connect_to_server()
        self.ships = self.create_ships()
        self.gui(self.ships)

    def connect_to_server(self):
        """
        Initialize connection to server and get location of battleships
        :param self: the client
        :return: grid to create the board
        """
        self.socket.connect(ADDRESS)
        return self.send_and_receive(GET_BOARD_MESSAGE), self.send_and_receive(GET_TURN_MESSAGE)

    def send_and_receive(self, msg):
        """
        sends a message to the server through the socket and waits for a return
        :param msg: a string message to send to the server
        :return: the object from the server
        """
        message = msg.encode(FORMAT)
        msg_lenght = len(message)
        send_lenght = str(msg_lenght).encode(FORMAT)
        send_lenght += b' ' * (HEADER - len(send_lenght))  # pad to 64 bytes
        self.socket.send(send_lenght)
        self.socket.send(message)
        msg_lenght = self.socket.recv(HEADER).decode(FORMAT)
        if msg_lenght:  # check not none
            msg_lenght = int(msg_lenght)
            msg = self.socket.recv(msg_lenght).decode(FORMAT)
            object_from_server = json.loads(msg)
            return object_from_server

    def gui(self, grid_from_server):
        """
        creates the gui for the game
        :param grid_from_server: ships location generated from the server
        :return: void
        """
        self.screen = create_gui(grid_from_server, self.my_grid_rectangles, self.opponent_rectangles,
                                 self.opponent_name, self.turn)

    def create_ships(self):
        ships = []
        for ship_indexes in self.ships_indexes:
            ship = Ship.Ship(ship_indexes[0], ship_indexes[1])
            ships.append(ship)
        return ships

    def handle_game(self):
        done = False
        font_fade = pygame.USEREVENT + 1
        show_text = False
        pygame.time.set_timer(font_fade, 800)
        while not done:
            # TODO : get message from server that game starts and cancel wait for opponent
            # TODO : get message from server to make a move
            # TODO : get message from server to check opponent move
            # TODO : get message from server to get hit or miss
            # TODO : get message for win
            # TODO : get message for loose
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if self.turn and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # mouse left button pressed
                    pos = pygame.mouse.get_pos()
                    x, y = ClientCalcUtils.check_rectangle_pressed(self.opponent_rectangles, pos)  # can be none
                    print(x, y)
                    if x is not None and y is not None:
                        pygame.display.iconify()
                        self.send_and_receive("TRY HIT " + str(x) + " " + str(y))
                if not self.turn:
                    pygame.display.iconify()
                if event.type == font_fade:
                    show_text = not show_text
                    if self.turn:
                        text_to_show = YOUR_TURN
                        color = BLUE
                    else:
                        text_to_show = OPPONENT_TURN
                        color = WHITE
                    if show_text:
                        draw_text(self.screen, text_to_show, color, 10, 530, 32)
                    else:
                        draw_blink_rect(self.screen, BLACK, 10, 530, text_to_show)

            pygame.display.flip()

        pygame.quit()
        self.send_and_receive(DISCONNECT_MESSAGE)


client = Client()
client.handle_game()
