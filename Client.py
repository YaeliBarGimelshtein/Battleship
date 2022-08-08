import json
import socket
import pygame
from ClientGuiUtils import create_gui, draw_text, draw_blink_rect, draw_rec_grid
import ClientCalcUtils
import Ship
import sys
import time

HEADER = 64  # each message will have a header to tell the message size
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"  # when receiving, close the connection and disconnect client
GET_BOARD_MESSAGE = "GET_BOARD"
GET_TURN_MESSAGE = "GET_TURN"
WAIT_TURN_MESSAGE = "WAIT_TURN"
TRY_HIT_MESSAGE = "TRY_HIT"
RESULT_HIT_MESSAGE = "RESULT_HIT"
GAME_OVER = "GAME_OVER"
IS_GAME_OVER = "IS_GAME_OVER"
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
        self.game_over = False
        self.screen = None
        self.ships_indexes, self.turn = self.connect_to_server()
        self.ships = self.create_ships()
        self.gui(self.ships)
        self.size_screen = (1, 1)

    def connect_to_server(self):
        """
        Initialize connection to server and get location of battleships
        :param self: the client
        :return: grid to create the board
        """
        self.socket.connect(ADDRESS)
        return self.send_and_receive(GET_BOARD_MESSAGE), self.send_and_receive(GET_TURN_MESSAGE)

    def send_and_receive(self, obj):
        """
        sends a message to the server through the socket and waits for a return
        :param obj: an object message to send to the server
        :return: the object from the server
        """
        obj_json = json.dumps(obj)
        msg_lenght = len(obj_json)
        obj_json = obj_json.encode(FORMAT)
        send_lenght = str(msg_lenght).encode(FORMAT)
        send_lenght += b' ' * (HEADER - len(send_lenght))  # pad to 64 bytes
        print("[CLIENT" + self.my_name + "] sent " + str(obj))
        self.socket.send(send_lenght)
        self.socket.send(obj_json)
        msg_lenght = self.socket.recv(HEADER).decode(FORMAT)
        if msg_lenght:  # check not none
            print("[CLIENT" + self.my_name + "] got message")
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
        self.screen, self.size_screen = create_gui(grid_from_server, self.my_grid_rectangles, self.opponent_rectangles,
                                                   self.opponent_name, self.turn)

    def create_ships(self):
        ships = []
        for ship_indexes in self.ships_indexes:
            ship = Ship.Ship(ship_indexes[0], ship_indexes[1])
            ships.append(ship)
        return ships

    def make_move(self):
        pos = pygame.mouse.get_pos()
        x, y = ClientCalcUtils.check_rectangle_pressed(self.opponent_rectangles, pos)  # can be none
        if x is not None and y is not None:
            self.send_and_receive(TRY_HIT_MESSAGE)
            hit_successful_indexes = self.send_and_receive((x, y))
            self.show_hit_result(hit_successful_indexes, x, y)
            draw_blink_rect(self.screen, BLACK, 10, 530, YOUR_TURN)
            pygame.display.flip()
            time.sleep(3)
            self.screen = pygame.display.set_mode(self.size_screen, pygame.HIDDEN)
            pygame.display.flip()
            self.game_over = self.send_and_receive(IS_GAME_OVER)
            if self.game_over:
                pygame.quit()

    def show_hit_result(self, hit_successful_indexes, row, column):
        if len(hit_successful_indexes[0]) == 0:
            color = BLACK
            rec = self.opponent_rectangles[row+1][column+1]
            draw_rec_grid(self.screen, color, rec.left, rec.top)
        else:
            for indexes in hit_successful_indexes:
                color = BLUE
                rec = self.opponent_rectangles[indexes[0]][indexes[1]] #Check if needed offset +1
                draw_rec_grid(self.screen, color, rec.left, rec.top)
        pygame.display.flip()

    def get_ship_hit(self, row, column):
        for ship in self.ships:
            if (row, column) in ship.indexes:
                return ship
        return None

    def check_opponent_move(self, row, column):
        hit_indexes = []
        is_hit = ClientCalcUtils.check_is_hit(self.my_grid_rectangles, row, column)
        if is_hit:
            ship = self.get_ship_hit(row, column)
            if ship is not None:
                ship.hit()
                is_ship_drown = ClientCalcUtils.check_is_ship_drown(ship)
                if is_ship_drown:  # dead ship
                    self.ships.remove(ship)  # comperator!!!
                    if len(self.ships) == 0:
                        self.game_over = True
                    return ship.indexes, self.game_over
                else:
                    hit_indexes.append((row, column))
                    return hit_indexes, self.game_over
        return hit_indexes, self.game_over

    def send_game_over(self):
        self.send_and_receive(GAME_OVER)
        pygame.quit()

    def handle_game(self):
        done = False
        font_fade = pygame.USEREVENT + 1
        show_text = False
        pygame.time.set_timer(font_fade, 800)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                if self.turn:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # mouse left button pressed
                        self.make_move()
                        self.turn = False

                if not self.turn:
                    row, column = self.send_and_receive(WAIT_TURN_MESSAGE)
                    indexes = self.check_opponent_move(row, column)
                    self.send_and_receive(RESULT_HIT_MESSAGE)
                    if self.game_over:
                        pygame.quit()
                    pygame.display.set_mode(self.size_screen, pygame.SHOWN)
                    pygame.display.flip()
                    self.send_and_receive(indexes)
                    self.turn = True

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
